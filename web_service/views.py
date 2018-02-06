from django.shortcuts import render
from .models import *
from .serializers import *

from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from annoying.functions import get_object_or_None
from datetime import date

from collections import namedtuple
import time
from datetime import datetime
from time import gmtime, strftime

# Create your views here.

@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user:
        serializer = UserSerializer(user)
        current_time = timezone.now()
        token = Token.objects.get(user=user)
        return JsonResponse({"user": serializer.data,
                             "token": token.key,
                             "login_time": strftime("%H:%M:%S", time.localtime())
                             }, status=200)
    else:
        return JsonResponse({"message": "invalid credentials"}, status=401)


@api_view(['GET'])
def logout(request):
    user= request.user
    if user:
        return JsonResponse({'message': 'User logged out successfully'})
    else:
        return JsonResponse({'message':'Unauthorized User'})


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user is None:
    	password = request.data['password']
    	user_save = User(
    		username = request.data['username']
    		)
    	user_save.set_password(password)
    	user_save.save()
    	user_role = Role(
    		user = user_save,
    		role_type = request.data['role'],
			department = request.data['department']
    		)
    	user_role.save()
    	return JsonResponse({'message': 'User registered successfully'}, status=201)
    return JsonResponse({'message': 'Username already Exists'})
        



########----Add new employee to the Organization-----########
class AddEmployeeView(APIView):
    def post(self, request):
        if request.data:
            email = request.data.get('email', None)
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            role = request.data.get('designation', None)
            department = request.data.get('department', None)
            phone_number = request.data.get('phone_no', None)
            if email:
                user = User.objects.filter(Q(username=email) | Q(email=email)).first()
                print(user)
                if user is None:
                    user_save = User(
                        first_name = first_name,
                        last_name = last_name,
                        username = email
                        )
                    user_save.save()
                    user_role = Role(
                        user = user_save,
                        role_type = role,
                        department = department
                        )
                    user_role.save()
                    request.data["user"] = user_save.id
                    print(request.data)
                    if user_save:
                        try:
                            serializer = AddNewEmployeeSerializer(data=request.data)
                            print('serializer', serializer)
                            if serializer.is_valid():
                                serializer.save()
                                return JsonResponse({'message':'User Added Successfully'}, status=200)
                        except(Exception)as e:
                            print('Exception',e)
                            user_save.delete()
                            user_role.delete()
                            pass
                        return JsonResponse({'message':'Bad String'}, status=400)
                    return JsonResponse({'message':'User Cannot be created, as details are not sufficient'}, status=400)
                return JsonResponse({'message':'User Already Exists'}, status=400)
            return JsonResponse({'message':'Email field is neccessory'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)
            

#######-----Approve New Employee----------###########
class ApproveEmployee(APIView):
    def get(self, request):
        employees = Employees.objects.filter(approved=False)
        employee_ids = [i.user.id for i in employees]
        print(employee_ids)
        users = User.objects.filter(id__in=employee_ids)
        print(users)
        serializer = ApproveEmployeesSerializer(users, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        _id = request.data.get('id', None)
        employee = Employees.objects.filter(user=_id).first()
        if employee:
            employee.approved = True
            employee.save()
            user_obj = User.objects.filter(id=employee.user.id).first()
            password = request.data.get('password', None)
            if password:
                user_obj.set_password(password)
            else:
                user_obj.set_password('dscignBiosys')
            user_obj.save()
            return JsonResponse({'message':'User activated, and password has set for the user account'}, status=200)
        return JsonResponse({'message':'Bad Request'}, status=400)


#######-----Add New Employee Ends---------############

class AttendanceCreate(APIView):
    def put(self, request):
        user = request.user
        if request.data['type'] == 1:
            attendance = Attendance.objects.create(user=user, clock_in=timezone.now())
            return JsonResponse({"message": "clocked in"}, status=200)
        elif request.data['type'] == 2:
            attendance = Attendance.objects.filter(user=user).order_by('-id')[0]
            attendance.clock_out = timezone.now()
            print(attendance.clock_out)
            attendance.save()
            return JsonResponse({"message": "clocked out"}, status=200)


class ActivityAddList(APIView):
    def post(self,request):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message" : "Activity Created Successfully"}, status = 201)
        else:
            print (serializer.errors)
            return JsonResponse({"message": "bad string"}, status=400)

    def put(self, request):
        
        try:
            activity = Activity.objects.get(id=request.data['id'])
            serializer = UpadteActivitySerializer(activity, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": 'Success'}, status=200)
            else:
                print (serializer.errors)
                return JsonResponse({"message": "bad string"}, status=400)
        except(ObjectDoesNotExist)as e:
            return JsonResponse({'message':'Requested Activity Does Not Exist'}, status=400)

    def get(self, request):
        if request.user.user_role.role_type == 'Employee':
            print(request.user)
            activities = Activity.objects.filter(created_by=request.user)
            serializer = ActivityFarmerMobSerializer(activities, many=True)
            return JsonResponse({'activities': serializer.data},
                                status=200)
        elif request.user.user_role.role_type == 'Manager':
            user_list = \
                Role.objects.filter(department=request.user.user_role.department)
            user_ids = [i.user_id for i in user_list]
            activities = \
                Activity.objects.filter(created_by_id__in=user_ids)
            serializer = ActivityFarmerMobSerializer(activities, many=True)
            return JsonResponse({'activities': serializer.data},
                                status=200)
        else:
            return JsonResponse({'activities': 'Not Found'}, status=405)

    def delete(self, request):
        try:
            activity_id = request.data['id']
        except(KeyError)as e:
            activity_id = None
        activity = Activity.objects.filter(id=activity_id).first()
        if activity:
            activity.delete()
            return JsonResponse({'message': 'Activity Deleted Successfully'}, status=200)
        return JsonResponse({'message': 'Not Found'}, status=405)

class DeleteActivity(APIView):
    def get(self, request, activity_id):
        print('Individual Activty')
        activity = Activity.objects.filter(id=activity_id).first()
        if activity:
            serializer = ActivitySerializer(activity, many=False)
            return Response(serializer.data)
        return JsonResponse({'message':'Not Found'}, status=405)


    def delete(self, request, activity_id):
        activity = Activity.objects.filter(id=activity_id).first()
        if activity:
            activity.delete()
            return JsonResponse({'message': 'Activity Deleted Successfully'}, status=200)
        return JsonResponse({'message': 'Not Found'}, status=405)


class ActivityGetList(APIView):
    def get(self, request, year, month, day):
        
        date_new = year+'-'+month+'-'+day
        print(date_new)
        if request.user.user_role.role_type == 'Employee':
            activities = Activity.objects.filter(created_by=request.user.id, activity_date__month=month, activity_date__year=year, activity_date__day=day)
            print('activities')
            serializer = ActivityFarmerMobSerializer(activities, many=True)
            return JsonResponse({'activities': serializer.data},
                                status=200)
        elif request.user.user_role.role_type == 'Manager':
            user_list = \
                Role.objects.filter(department=request.user.user_role.department)
            user_ids = [i.user_id for i in user_list]
            activities = \
                Activity.objects.filter(created_by_id__in=user_ids, activity_date=date_new)
            serializer = ActivityFarmerMobSerializer(activities, many=True)
            return JsonResponse({'activities': serializer.data},
                                status=200)
        else:
            return JsonResponse({'activities': 'Not Found'}, status=405)



class ExpenseAddList(APIView):
    def get(self, request):
        if request.user.user_role.role_type == 'Employee':
            expenses = Expense.objects.filter(created_by=request.user)
            serializer = ExpenseSerializer(expenses, many=True)
            return JsonResponse({"expenses": serializer.data}, status=200)
        elif request.user.user_role.role_type == 'Manager':
            user_list = Role.objects.filter(department=request.user.user_role.department)
            user_ids = [i.user_id for i in user_list]
            expenses = Expense.objects.filter(created_by_id__in=user_ids)
            serializer = ExpenseSerializer(expenses, many=True)
            return JsonResponse({"expenses": serializer.data}, status=200)

    def post(self,request):

        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Expense Added Successfully"}, status=200)
        else:
            print (serializer.errors)
            return JsonResponse({"message": "bad string"}, status=400)

    def put(self, request):
        try:
            expense = Expense.objects.get(id=request.data['id'])
            serializer = ExpenseSerializer(expense, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "success"}, status=200)
            else:
                print(serializer.errors)
                return JsonResponse({"message": "bad string"}, status=400)
        except(ObjectDoesNotExist)as e:
            return JsonResponse({'message':'Requested expense Does Not Exist'}, status=400)

    def delete(self, request):
        try:
            expense_id = request.data['id']
        except(KeyError)as e:
            expense_id = None

        if expense_id:
            expense = Expense.objects.filter(id = expense_id).first()
            expense.delete()
            return JsonResponse({'message':'Expense Deleted Successfully'}, status=200)
        return JsonResponse({'message':'Expense Not Found'}, status=404)



class ExpenseIndividual(APIView):
    def get(self, request, user_id):
        expenses = Expense.objects.filter(created_by=user_id)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

class ManagerExpenseView(APIView):
    def get(self, request):
        if request.user.user_role.role_type == 'Manager':
            user_list = Role.objects.filter(department=request.user.user_role.department)
            user_ids = [i.user_id for i in user_list]
            applied_expense = Expense.objects.filter(created_by__in=user_ids)
            appliedExpenseUsers = [i.created_by.id for i in applied_expense]
            print(appliedExpenseUsers[0])
            expense = User.objects.filter(id__in = appliedExpenseUsers)
            serializer = EmployeesExpenseForManager(expense, many=True)
            return Response(serializer.data)
        return JsonResponse({'message':'Unauthorized Access'})



@api_view(['POST'])
def approve_expense(request):
    applied_expense = get_object_or_None(Expense, id=request.data['id'], status=False, declined=False)
    user = get_object_or_None(User, id=request.data['user_id'])
    if user:
        if applied_expense:
            applied_expense.status = request.data['status']
            applied_expense.save()
            if applied_expense.status:
                applied_expense.aproved_by = user
                applied_expense.approvedOn = timezone.now()
                applied_expense.actionOn = timezone.now()
                applied_expense.save()
                return JsonResponse({'message': 'Approved Expense'}, status=200)
            else:
                applied_expense.declined = True
                applied_expense.actionOn = timezone.now()
                applied_expense.save()
                return JsonResponse({'message': 'Expense Application Declined'}, status=200)
        else:
            return JsonResponse({"message": "Either Expense is Invalid Or Expense Expired"}, status=400)
    else:
        return JsonResponse({"message": "Unauthorized User"}, status=403)



"""leavemanagement"""


class HolidayView(APIView):
    """
    Holiday CRUD operation
    """

    def get(self, request, format=None):
        holiday = Holiday.objects.all()
        if holiday:
            serializers = HolidaySerializer(holiday, many=True)
            return Response(serializers.data)
        return JsonResponse({'message': 'Not Found'}, status=405)

    def post(self, request, format=None):
        if request.data:
            serializer = HolidaySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Holiday saved successfully'}, status=200)
            return JsonResponse({'message': 'Bad request'}, status=400)
        return JsonResponse({'message': 'Bad request'}, status=400)


class MainLeaveView(APIView):
    """
    Assign Leave and List Leave
    """

    def get(self, request, format=None):
        # username = request.user.username
        leaves = Leaves.objects.all()
        if leaves:
            serializer = LeavesSerializer(leaves, many=True)
            return Response(serializer.data)
        return JsonResponse({'message': 'Not Found'}, status=404)

    def post(self, request, format=None):
        if request.data:
            user = User.objects.filter(id=request.data['user_id']).first()
            if user:
                try:
                    leaves_instance = Leaves(
                        balance_sick_leave=request.data['total_sick_leave'],
                        total_sick_leave=request.data['total_sick_leave'],
                        balance_casual_leave=request.data['total_casual_leave'],
                        total_casual_leave=request.data['total_casual_leave'],
                        balance_earned_leave=request.data['total_earned_leave'],
                        total_earned_leave=request.data['total_earned_leave'],
                        balance_compoff_leave=request.data['total_compoff_leave'],
                        total_compoff_leave=request.data['total_compoff_leave'],
                        user=user
                    )
                    leaves_instance.save()
                except(KeyError, AttributeError, TypeError)as e:
                    pass
                return JsonResponse({'message': 'Leave assigned successfully'}, status=200)
            return JsonResponse({'message': 'User Not Found'}, status=405)
        return JsonResponse({'message': 'Bad Request'}, status=400)


class AppliedLeaveViewAPI(APIView):
    """
    Applied Leave Class
    """

    def get(self, request, format=None):
        applied_leave = AppliedLeave.objects.filter(status=False, declined=False)
        if applied_leave:
            serializer = AppliedLeaveListSerializer(applied_leave, many=True)
            return Response(serializer.data)
        return JsonResponse({'message': 'Not Found'}, status=404)

    def put(self, request, format=None):
        if request.data:
            print(request.data['id'])
            applied_leave = AppliedLeave.objects.filter(id=request.data['id']).first()
            if applied_leave:
                serializer = AppliedLeaveUpdate(applied_leave, data=request.data)
                print(serializer)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message': 'Updated Successfully'}, status=200)
                return JsonResponse({'message':'Bad String'}, status=405)
            return JsonResponse({'message': 'Leave Not Found'}, status=404)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request, format=None):
        if request.data:
            applied_leave = AppliedLeave.objects.filter(id=request.data['id']).first()
            if applied_leave:
                applied_leave.delete()
                return JsonResponse({'message': 'Leave Deleted Successfully'}, status=200)
            return JsonResponse({'message': 'Leave Not Found'}, status=404)
        return JsonResponse({'message':'Bad Request'}, status=400)


class LeaveUserInfo(APIView):
    def get(self, request, user_id, month, year):
        leave_info = []
        user = User.objects.filter(id=user_id).first()
        if user:
            holidays = Holiday.objects.filter(date__month=month, date__year=year)
            for h in holidays:
                holiday ={
                    'id': h.id,
                    'reason': h.reason,
                    'date': h.date,
                    'type': 'Official'
                }
                leave_info.append(holiday)
            applied_leave = AppliedLeave.objects.filter(user=user, appliedOn__month=month, appliedOn__year=year).all()
            for a in applied_leave:
                applied={
                    'id': a.id,
                    'type_of_leave':a.type_of_leave,
                    'leave_from': a.leave_from,
                    'to_leave': a.to_leave,
                    'number_of_days': a.number_of_days,
                    'status': a.status,
                    'appliedOn':a.appliedOn,
                    'declined':a.declined,
                    'reason': a.reason,
                    'type': 'Applied'
                }
                leave_info.append(applied)
            return JsonResponse({'leave_info': leave_info}, status=200)
        return JsonResponse({'message': 'Un-Recognised User'}, status=400)



class AppliedLeaveUserHistory(APIView):
    def get(self, request, user_id):
        applied_leave = AppliedLeave.objects.filter(appliedBy=user_id)
        serializer = AppliedLeaveHistory(applied_leave, many=True)
        return Response(serializer.data)



@api_view(['GET'])
def leave_info_user(id, *args, **kwargs):
    user = User.objects.filter(id=id).first()
    print(user)
    return JsonResponse({'message': 'Leave assigned successfully'}, status=200)


class EmployeeBalanceLeave(APIView):
	"""
	Check Balance Leave Of Individual Employee
	"""
	def get(self, request, user_id, format=None):
		user = User.objects.filter(id=user_id).first()
		if user:
			leaves = Leaves.objects.filter(user=user).first()
			print(leaves.balance_sick_leave)
			if leaves:
				serializer = BalanceLeaveSerializer(leaves)
				return Response(serializer.data)
			else:
				return JsonResponse({'message':'Leaves Not Found'}, status=405)
		else:
			return JsonResponse({'message': 'User Not Found'}, status=405)


@api_view(['POST'])
def apply_leave(request):
    if request.data:
        user = User.objects.filter(id=request.data['user']).first()
        try:
            reason = request.data['reason']
        except(KeyError, AttributeError)as e:
            reason = " "

        try:
           number_of_days =  request.data['number_of_days']
        except(KeyError, AttributeError)as e:
            number_of_days = None

        try:
           type_of_leave =  request.data['type_of_leave']
        except(KeyError, AttributeError)as e:
            type_of_leave = None

        try:
           leave_from =  request.data['leave_from']
        except(KeyError, AttributeError)as e:
            leave_from = None

        try:
           to_leave =  request.data['to_leave']
        except(KeyError, AttributeError)as e:
            to_leave = None

        if user:
            try:
                apply_leave_instance = AppliedLeave(
                    user=user,
                    type_of_leave=type_of_leave,
                    leave_from=leave_from,
                    to_leave=to_leave,
                    number_of_days=number_of_days,
                    reason = reason,
                    appliedBy=user
                )
                apply_leave_instance.save()
            except(KeyError, AttributeError, TypeError)as e:
                pass
            return JsonResponse({'message': 'Leave Applied Successfully'}, status=200)
        return JsonResponse({'message': 'User Not Found'}, status=405)
    return JsonResponse({'message': 'Bad Request'}, status=400)


def update_balance_leave(user, typeOfLeave, days):
    leave = Leaves.objects.filter(user=user).first()
    leave_type = 'balance_' + typeOfLeave
    col_value = getattr(leave, leave_type)
    if col_value is not None:

        if leave_type == 'balance_compoff_leave':
            print('in balance compoff')
            bal = float(col_value) + float(days)
            updateLeaves = Leaves.objects.filter(user=user).update(**{leave_type: bal, 'total_compoff_leave': bal})
            message = 1
        else:
            bal = float(col_value) - float(days)
            if bal<0:
                updateLeaves = Leaves.objects.filter(user=user).update(**{leave_type: 0})
                bal = abs(bal)
                print(bal)
                lop_add = EmployeeLop(
                    user = user,
                    count = bal
                    )
                lop_add.save()
            else:
                updateLeaves = Leaves.objects.filter(user=user).update(**{leave_type: bal})
            message = 1
    else:
        message = 2
    return message


@api_view(['PUT'])
def approve_leave(request):
    applied_leave = get_object_or_None(AppliedLeave, id=request.data['leave_id'], status=False, declined=False)
    user = get_object_or_None(User, id=request.data['user'])
    if user:
        if applied_leave:
            applied_leave.status = request.data['approval_status']
            if applied_leave.status:
                applied_leave.approvedBy = user
                applied_leave.approvedOn = timezone.now()
            applied_leave.actionOn = timezone.now()

            if applied_leave.status:
                # leave_bal = Leaves.objects.get(user=applied_leave.appliedBy)
                updating_leave = update_balance_leave(applied_leave.appliedBy, applied_leave.type_of_leave,
                                                      applied_leave.number_of_days)
                if updating_leave == 1:
                    applied_leave.save()
                    return JsonResponse({'message': 'Approve Leave and Updated Balance Leave'}, status=204)
                elif updating_leave == 2:
                    return JsonResponse({'message': 'Invalid Leave'}, status=400)
            else:
                applied_leave.declined = True
                applied_leave.save()
                return JsonResponse({'message': 'Leave Application Declined'}, status=200)
        else:
            return JsonResponse({"message": "Either Leave is Invalid Or Leave Expired"}, status=400)
    else:
        return JsonResponse({"message": "Unauthorized User"}, status=403)





class ManagerLeaveView(APIView):    
    def get(self, request):
        if request.user.user_role.role_type == 'Manager':
            user_list = Role.objects.filter(department=request.user.user_role.department)
            user_ids = [i.user_id for i in user_list]
            applied_leave = AppliedLeave.objects.filter(appliedBy__in=user_ids)
            appliedLeaveUsers = [i.user_id for i in applied_leave]
            print(appliedLeaveUsers)
            leaves = User.objects.filter(id__in=appliedLeaveUsers)
            serializer = EmployeesLeaveForManager(leaves, many=True)
            return Response(serializer.data)
        return JsonResponse({'message':'Unauthorized Access'})




#######################------------Forms----------------#####################


@api_view(['POST'])
def add_farmer_details(request):
    if request.data:
        try:
            farmer_activity = FarmerDetails.objects.filter(activity=request.data['activity_id']).first()
        except(KeyError)as e:
            farmer_activity=None

        if farmer_activity is None:
            try:
                activity = Activity.objects.filter(id=request.data['activity_id']).first()
            except(KeyError, AttributeError)as e:
                activity = None

            if request.data['user_id']:
                user = User.objects.filter(id=request.data['user_id']).first()
                if user:
                    try:
                        farmer_name = request.data['farmer_name']
                    except(KeyError)as e:
                        farmer_name = None

                    try:
                        state = request.data['state']
                    except(KeyError)as e:
                        state = None

                    try:
                        district = request.data['district']
                    except(KeyError)as e:
                        district = None

                    try:
                        taluka = request.data['taluka']
                    except(KeyError)as e:
                        taluka = None

                    try:
                        address = request.data['address']
                    except(KeyError)as e:
                        address = None

                    try:
                        longitude = request.data['longitude']
                    except(KeyError)as e:
                        longitude = None

                    try:
                        latitude = request.data['latitude']
                    except(KeyError)as e:
                        latitude = None

                    try:
                        primary_phone = request.data['primary_phone']
                    except(KeyError)as e:
                        primary_phone = None

                    try:
                        secondary_phone = request.data['secondary_phone']
                    except(KeyError)as e:
                        secondary_phone = None

                    try:
                        email = request.data['email']
                    except(KeyError)as e:
                        email = None

                    try:
                        land_area = request.data['land_area']
                    except(KeyError)as e:
                        land_area = None

                    try:
                        soil_color = request.data['soil_color']
                    except(KeyError)as e:
                        soil_color = None

                    try:
                        pin = request.data['pin']
                    except(KeyError)as e:
                        pin = None

                    try:
                        soilType = request.data['soil_type']
                    except(KeyError)as e:
                        soilType = None

                    try:
                        cropType = request.data['crop_type']
                    except(KeyError)as e:
                        cropType = None

                    form = FarmerDetails(
                        activity = activity,
                        created_by = user,
                        farmer_name = farmer_name,
                        state = state,
                        district = district,
                        taluka = taluka,
                        address = address,
                        pin = pin,
                        longitude = longitude,
                        latitude = latitude,
                        primary_phone = primary_phone,
                        secondary_phone = secondary_phone,
                        email = email,
                        land_area = land_area,
                        soil_color = soil_color
                        )
                    form.save()
                    if soilType is not None:
                        for a in soilType:
                            soilItems = FarmerSoilType(
                                farmer=form,
                                soil = a['soil']
                                )
                            soilItems.save()
                    if cropType is not None:
                        for b in cropType:
                            cropItems = FarmerCropType(
                                farmer = form,
                                crop = b['crop']
                                )
                            cropItems.save()
                    return JsonResponse({'message': 'Farmer Details Added Successfully'}, status=200)
                else:
                    return JsonResponse({'message':'Unauthorized Access, Cannot Recognise User'}, status=405)
            else:
                return JsonResponse({'message': 'Unauthorized Request'}, status=400)
        else:
            return JsonResponse({'message': 'Sorry, Cannot Have multiple farmer details for one activity, create one Activity'})
    else:
        return JsonResponse({'message': 'Bad Request'}, status=400)


class FarmerDetailsClass(APIView):
    def get(self, request):
        farmer_details_obj = FarmerDetails.objects.all()
        if farmer_details_obj:
            serializer = FarmerDetailsSerializer(farmer_details_obj, many=True)
            if serializer:
                return Response(serializer.data)
            return JsonResponse({'message': 'Something Went Wrong'}, status=400)
        return JsonResponse({'message': 'Not Found'}, status=405)

class FarmerDetailsIndividual(APIView):
    def get(self, request, activity_id, user_id):
        farmer_obj = FarmerDetails.objects.filter(activity=activity_id, created_by=user_id).first()
        if farmer_obj:
            serializer = FarmerDetailsSerializer(farmer_obj)
            if serializer:
                return Response(serializer.data)
            return JsonResponse({'message': 'Something Went Wrong'}, status=400)
        return JsonResponse({'message': 'Not Found'}, status=405)


class FarmerDetailsUser(APIView):
    def get(self, request, user_id):
        farmer_obj = FarmerDetails.objects.filter(created_by=user_id).all()
        # print(farmer_obj[0].activity)
        if farmer_obj:
            serializer = FarmerDetailsSerializer(farmer_obj, many=True)
            if serializer:
                return Response(serializer.data)
            return JsonResponse({'message': 'Something Went Wrong'}, status=400)
        return JsonResponse({'message': 'Not Found'}, status=400)


class FarmerListViewBasedOnUserDate(APIView):
    def get(Self, request, user_id, year, month, day):
        date_new = year+'-'+month+'-'+day
        user = User.objects.filter(id=user_id).first()
        if user.user_role.role_type=='Employee':
            # print(date_new)
            # farmer = FarmerDetails.objects.filter(created_by=user_id, form_filled_on__year=year, form_filled_on__month=month, form_filled_on__day=day).all()
            farmer = FarmerDetails.objects.filter(created_by=user_id, form_filled_on = date_new).all()
            serializer = FarmerDetailsSerializer(farmer, many=True)
            return Response(serializer.data)

        elif user.user_role.role_type== 'Manager':
            farmer = FarmerDetails.objects.filter(form_filled_on = date_new).all()
            serializer = FarmerDetailsSerializer(farmer, many=True)
            return Response(serializer.data)


class FarmerListViewBasedOnUser(APIView):
    def get(Self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if user.user_role.role_type=='Employee':
            # print(date_new)
            # farmer = FarmerDetails.objects.filter(created_by=user_id, form_filled_on__year=year, form_filled_on__month=month, form_filled_on__day=day).all()
            farmer = FarmerDetails.objects.filter(created_by=user_id).all()
            serializer = FarmerDetailsSerializer(farmer, many=True)
            return Response(serializer.data)

        elif user.user_role.role_type== 'Manager':
            farmer = FarmerDetails.objects.filter().all()
            serializer = FarmerDetailsSerializer(farmer, many=True)
            return Response(serializer.data)


@api_view(['PUT'])
def upadte_farmer_details_form(request):
    # if request.data:
    #     farmer = FarmerDetails.objects.filter(id =request.data['id']).first()
    #     updating = UpdateFarmerDetails(farmer, data=request.data)
        
    #     if updating.is_valid():
    #         return Response(updating.data)
    #     print(updating.errors)
    #     return JsonResponse({'message':'Something Went Wrong'})
    try:
        farmer_obj = FarmerDetails.objects.filter(id=request.data["id"]).first()
    except(KeyError)as e:
        farmer_obj = None

    if farmer_obj:
        try:
            farmer_name = request.data['farmer_name']
        except(KeyError)as e:
            farmer_name = None

        try:
            state = request.data['state']
        except(KeyError)as e:
            state = None

        try:
            district = request.data['district']
        except(KeyError)as e:
            district = None

        try:
            taluka = request.data['taluka']
        except(KeyError)as e:
            taluka = None

        try:
            address = request.data['address']
        except(KeyError)as e:
            address = None

        try:
            longitude = request.data['longitude']
        except(KeyError)as e:
            longitude = None

        try:
            latitude = request.data['latitude']
        except(KeyError)as e:
            latitude = None

        try:
            primary_phone = request.data['primary_phone']
        except(KeyError)as e:
            primary_phone = None

        try:
            secondary_phone = request.data['secondary_phone']
        except(KeyError)as e:
            secondary_phone = None

        try:
            email = request.data['email']
        except(KeyError)as e:
            email = None

        try:
            land_area = request.data['land_area']
        except(KeyError)as e:
            land_area = None

        try:
            soil_color = request.data['soil_color']
        except(KeyError)as e:
            soil_color = None

        try:
            pin = request.data['pin']
        except(KeyError)as e:
            pin = None

        try:
            soilType = request.data['soil_type']
        except(KeyError)as e:
            soilType = None

        try:
            cropType = request.data['crop_type']
        except(KeyError)as e:
            cropType = None

        FarmerDetails.objects.filter(id=request.data["id"]).update(
                                                farmer_name=farmer_name,
                                                state = state,
                                                district = district,
                                                taluka = taluka,
                                                address = address,
                                                pin = pin,
                                                longitude = longitude,
                                                latitude = latitude,
                                                primary_phone = primary_phone,
                                                secondary_phone = secondary_phone,
                                                email = email,
                                                land_area = land_area,
                                                soil_color = soil_color
                                                )

        try:
            if request.data["soil_type"]:
                try:
                    update_soil_type(farmer_obj, request.data["soil_type"])
                except(KeyError, TypeError, AttributeError)as e:
                    pass
            else:
                pass
        except(KeyError)as e:
            pass

        try:
            if request.data["crop_type"]:
                try:
                    update_crop_type(farmer_obj, request.data["crop_type"])
                except Exception as e:
                    pass
            else:
                pass
        except(KeyError)as e:
            pass
        return JsonResponse({'message':'Farmers Details Updated Successfully'}, status=200)
    return JsonResponse({'message':'Bad Request'}, status=400)


def update_soil_type(farmer, soil_obj):
    if soil_obj:
        try:
            print(soil_obj)
            for s in soil_obj:
                FarmerSoilType.objects.filter(id=s["id"], farmer=farmer).update(soil = s["soil"])
        except Exception as e:
            pass
        return 1

def update_crop_type(farmer, crop_obj):
    if crop_obj:
        try:
            
            for c in crop_obj:
                FarmerCropType.objects.filter(id = c["id"], farmer=farmer).update(crop=c["crop"])
        except Exception as e:
            pass
        return 1

####################-----------------Form 2-----------------------########################

class CultivationFormView(APIView):
    def post(self, request):
        if request.data:
            serializer = CultivationFormSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Cultivation form saved'}, status=200)
            return JsonResponse({'message':'Bad request'}, status=400)
        return JsonResponse({'message': 'Bad String'}, status=400)

    def get(self, request):
        cult_form = CultivationForm.objects.all()
        if cult_form:
            serializer = CultivationFormReadSerializer(cult_form, many =True)
            return Response(serializer.data)
        return JsonResponse({'message':'Not Found'}, status=404)

    def put(self, request):
        cult_form = CultivationForm.objects.filter(id =request.data["id"]).first()
        if cult_form and request.data:
            serializer = CultivationFormSerializer(cult_form, data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Cultivation Form Updated'}, status=204)
            return JsonResponse({'message':'Bad request'}, status=400)
        return JsonResponse({'message': 'Bad String'}, status=400)

    def delete(self, request):
        cult_form = CultivationForm.objects.filter(id=request.data['id']).first()
        if cult_form:
            cult_form.delete()
            return JsonResponse({'message':'Cultivation Form Deleted Successfully'}, status=200)
        return JsonResponse({'message':'Cultivation Form Not Found'}, status=400)

class CultivationGetView(APIView):
    def get(self, request, farmer_id):
        cult_form = CultivationForm.objects.filter(farmer=farmer_id).all()
        if cult_form:
            serializer = CultivationFormReadSerializer(cult_form, many=True)
            return Response(serializer.data)
        return JsonResponse({'message': 'Not Found'}, status=404)



######################------------------Form 3-----------------######################

class SampleFormView(APIView):
    # def post(self, request):
    #     if request.data:
    #         serializer = SampleFormSerializer(data=request.data)
    #         print(serializer)
    #         if serializer.is_valid():
    #             print("saved")
    #             serializer.save()
    #             return JsonResponse({'message': 'Sample Form saved Successfully'}, status=200)
    #         return JsonResponse({'message':'Bad request'}, status=400)
    #     return JsonResponse({'message': 'Bad String'}, status=400)
    def post(self, request):
        if request.data:
            serializer = SampleFormSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Sample Form saved'}, status=200)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)
        # if request.data:
        #     # print(request.data)
        #     data = request.data
        #     if request.data['excepted_result_date']:
        #         expected_result_date = request.data['excepted_result_date']
        #     else:
        #         excepted_result_date = None

        #     farmer =FarmerDetails.objects.filter(id=data['farmer']).first()
        #     if farmer:
        #         sample = SampleForm(
        #                 farmer=farmer,
        #                 previous_year=data["previous_year"],
        #                 sample = data["sample"],
        #                 quantity = data["quantity"],
        #                 sample_request = data["sample_request"],
        #                 sample_request_qauntity = data["sample_request_qauntity"],
        #                 photo_upload= data["photo_upload"],
        #                 excepted_result_date = data["excepted_result_date"],
        #                 excepted_result_photo = data["excepted_result_photo"],
        #                 excepted_result_note = data["excepted_result_note"]
        #             )
        #         sample.save()
        #         return JsonResponse({'message': 'Sample Form saved Successfully'}, status=200)
        #     else:
        #         pass
        # return JsonResponse({'message':'Bad request'}, status=400)

    def get(self, request):
        sample_form = SampleForm.objects.all()
        if sample_form:
            serializer = SampleFormSerializer(sample_form, many=True)
            return Response(serializer.data)
        return JsonResponse({'message':'Not Found'}, status=404)

    def put(self, request):
        # cult_form = CultivationForm.objects.filter(id =request.data["id"]).first()
        if request.data:
            for data in request.data:
                sample_form_obj = SampleForm.objects.filter(id=data["id"]).first()
                if sample_form_obj:
                    serializer = SampleFormSerializer(sample_form_obj,data=data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        pass
                else:
                    pass
            return JsonResponse({'message': 'sample Updated'}, status=204)
        return JsonResponse({'message': 'Bad String'}, status=400)

    def delete(self, request):
        if request.data:
            sample = SampleForm.objects.filter(id = request.data['id']).first()
            if sample:
                sample.delete()
                return JsonResponse({'message':'Sample Form Deleted Successfully'}, status=200)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)  

class SampleFarmerFormView(APIView):
    def get(self, request, farmer_id):
        sample_form = SampleForm.objects.filter(farmer=farmer_id)
        if sample_form:
            serializer = SampleFormSerializer(sample_form, many=True)
            return Response(serializer.data)
        return JsonResponse({'message': 'Not Found'}, status=404)

class SampleIndividualForm(APIView):
    def get(self, request, id):
        sample_form = SampleForm.objects.filter(id=id).first()
        if sample_form:
            serializer = SampleFormSerializer(sample_form)
            return Response(serializer.data)
        return JsonResponse({'message': 'Not Found'}, status=404)


###############################--Sample And Cultivation Based on Farmer Id---#######################
class CultivationSampleFormView(APIView):
    def get(self, request, farmer_id):
        Farmer = namedtuple('Farmer', ('farmer_sample', 'farmer_cultivation'))
        cult_sample_form = Farmer(
            farmer_sample = SampleForm.objects.filter(farmer=farmer_id),
            farmer_cultivation = CultivationForm.objects.filter(farmer=farmer_id),
            )
        serializer = CultivationSample(cult_sample_form)
        return Response(serializer.data)



##############################Dealer Form###########################
class DealerFormView(APIView):
    def post(self, request):
        if request.data:
            serializer = DealerFormSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Dealer Details saved Successfully'}, status=200)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad request'}, status=400)

    def get(self, request):
        dealer = DealerForm.objects.all()
        if dealer:
            serializer = DealerFormSerializer(dealer, many=True)
            return  Response(serializer.data)
        return JsonResponse({'message':'Not Found'}, status=405)

    def put(self, request):
        dealer = DealerForm.objects.filter(id=request.data['id']).first()
        if dealer:
            serializer = DealerFormSerializer(dealer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Dealer Updated successfully'}, status=204)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message': 'Bad Request, Dealer Not found'}, status=405)

class DealerIndividual(APIView):
    def get(self, request, id):
        dealer = DealerForm.objects.filter(id=id).first()
        if dealer:
            serializer = DealerFormSerializer(dealer)
            return Response(serializer.data)
        return JsonResponse({'message':'Not Found'}, status=405)


#####################----------------Vendor-----------------############################
class VendorDetails(APIView):
    def post(self, request):
        if request.data:
            vendor = Vendors(
                vendor_name = request.data['vendor_name'],
                vendor_address = request.data['vendor_address'],
                vendor_city = request.data['vendor_city'],
                vendor_pin_code = request.data['vendor_pin_code'],
                vendor_pan = request.data['vendor_pan'],
                vendor_gst = request.data['vendor_gst'],
                vendor_contact = request.data['vendor_contact'],
                vendor_po = request.data['vendor_po'],
                vendor_po_date = request.data['vendor_po_date'],
                )
            vendor.save()

            for item in request.data['orders']:
                order_item = Orders(
                        vendor=vendor,
                        item_code = item['item_code'],
                        hsn_sac_code = item['hsn_sac_code'],
                        item_name = item['item_name'],
                        description = item['description'],
                        uom = item['uom'],
                        qty = item['qty'],
                        rate = item['rate'],
                        discount_amount = item['discount_amount'],
                        total_amount = item['total_amount'],
                    )
                order_item.save()
            return JsonResponse({'message': 'Order Plced Successfully'}, status=200)
        return JsonResponse({'message': 'Bad Request'}, status=400)

    def get(self, request):
        vendors = Vendors.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

class VendorsIndividiual(APIView):
    def get(self, request, id):
        vendor = Vendors.objects.filter(id = id).first()
        serializer = VendorSerializer(vendor, many=False)
        return Response(serializer.data)

    def put(self, request, id):
        vendor = Vendors.objects.filter(id=id).first()
        serializers = VendorSerializer(vendor, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse({'message':'Vendor Details Updated Successfully'}, status=204)
        return JsonResponse({'message': 'Something Wend Wrong'}, status=400)


    def delete(self, request, id):
        vendor = Vendors.objects.filter(id=id).first()
        if vendor:
            vendor.delete()
            return JsonResponse({'message': 'Vendor Deleted Successfully'}, status=200)
        return JsonResponse({'message': 'Vendor Not Valid'})



#####################----------------Order-------------------#############################
class OrderPlacingView(APIView):
    def post(self, request):
        if request.data:
            serializer = OrderPlacingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Order Plced Successfully'}, status=200)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message': 'Bad Request'}, status=400)

    def get(self, request):
        order = Orders.objects.all()
        serializer = OrderPlacingSerializer(order, many=True)
        return Response(serializer.data)





####################------------Order Placing-----------------#############################
class VendorCreateView(APIView):
    def post(self, request, format=None):
        if request.data:
            serializer = VendorCreate(data=request.data)
            print('serializer',serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        vendors = Vendors.objects.all()
        serializer = VendorListSerializer(vendors, many=True)
        return Response(serializer.data)

    def delete(self, request, format=None):
        if request.data:
            vendor = Vendors.objects.filter(id=request.data['id'])
            if vendor:
                vendor.delete()
                return JsonResponse({'message':'Vendor Deleted Successfully'})
            return JsonResponse({'message':'Not Found, Invalid Vendor Credential'}, status=404)
        return JsonResponse({'message':'Bad Response'}, status=400)

    def put(self, request, format=None):
        if request.data:
            vendor = Vendors.objects.filter(id=request.data['id']).first()
            if vendor:
                serializer = VendorCreate(vendor, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Vendor Details Updated Successfully'}, status=200)
                return JsonResponse({'message': 'Bad String'}, status=400)
            return JsonResponse({'message': 'Vendor not Found'}, status=404)
        return JsonResponse({ 'message' : 'Bad Request' }, status=400)


class ShippingAddressView(APIView):
    def post(self, request, format=None):
        if request.data:
            serializer = ShippingAddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def put(self, request, format=None):
        if request.data:
            address = ShippingAddress.objects.filter(id=request.data['id']).first()
            if address:
                serializer = ShippingAddressSerializer(address, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return JsonResponse({'message': 'Bad String'}, status=400)
            return JsonResponse({'message':'Not Found'}, status=404)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request, format=None):
        if request.data:
            address = ShippingAddress.objects.filter(id=request.data['id']).first()
            if address:
                address.delete()
                return JsonResponse({'message':'Shipping address Deleted Successfully'}, status=200)
            return JsonResponse({'message':'Not Found'}, status=404)
        return JsonResponse({'message':'Bad Request'}, status=400)

class ShippingAddressVendors(APIView):
    def get(self, request, vendor_id, format=None):
        vendor = Vendors.objects.filter(id=vendor_id).first()
        if vendor:
            address = ShippingAddress.objects.filter(vendor=vendor).all()
            serializer = ShippingAddressSerializer(address, many=True)
            return Response(serializer.data)
        return JsonResponse({'message':'Invalid Vendor'}, status=400)

class PlacingOrders(APIView):
    def post(self, request, format=None):
            # def post(self, request, format=None):
        if request.data:
            serializer = PlaceOrderSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Order Place Successfully'}, status=200)
            # return JsonResponse({'message': 'Bad String'}, status=400)
            return Response(serializer.errors)
        return JsonResponse({'message': 'Bad Request'}, status=400)

    def put(self, request, format=None):
        if request.data:
            # print(request.data['order_items'])
            orders = Orders.objects.filter(id = request.data['id']).first()
            serializer = PlaceOrderSerializer(orders, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Order Updated Successfully'}, status=200)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

##############-------------------------HR Payrole----------------------####################

class HrUserView(APIView):
    def get(self, request, format=None):
        if request.user.user_role.department == 'HR':
            employees = Role.objects.all()
            user_ids = [i.user_id for i in employees]
            users = User.objects.filter(id__in=user_ids)
            serializer = HrUserSerializer(users, many=True)
            return Response(serializer.data)

        # if request.user.user_role.role_type == 'Manager':
        #     user_list = Role.objects.filter(department=request.user.user_role.department)
        #     user_ids = [i.user_id for i in user_list]
        #     applied_expense = Expense.objects.filter(created_by__in=user_ids)
        #     appliedExpenseUsers = [i.created_by.id for i in applied_expense]
        #     print(appliedExpenseUsers[0])

class SalaryView(APIView):
    def post(self, request, format=None):
        if request.data:
            serializer = SalarySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Saved Salary of the Employee'}, status=200)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        salary = Salary.objects.all()
        serializer = SalarySerializer(salary, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        if request.data:
            salary = Salary.objects.filter(user=request.data['user']).first()
            if salary:
                serializer = SalarySerializer(salary, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Updated Salary of the employee'}, status=200)
                return JsonResponse({'message':'Bad String'}, status=400)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request, format=None):
        if request.data:
            salary = Salary.objects.filter(user=request.data['user']).first()
            if salary:
                salary.delete()
                return JsonResponse({'message':'Salary Deleted Successfully'}, status=200)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad String'}, status=400)


##############-------------------------Employee Document----------------------###################
class EmployeeDocumentView(APIView):
    def post(self, request):
        if request.data:
            serializer = EmployeeDocumentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return  JsonResponse({'message':'Document Uploaded Successfully'}, status=200)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)


    def get(self, request):
        documents = EmployeeDocument.objects.all()
        serializer = EmployeeDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def put(self, request):
        if request.data:
            try:
                document = EmployeeDocument.objects.get(id = request.data['id'])
                if document:
                    serializer = EmployeeDocumentSerializer(document, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'message':'Document Updated Successfully'}, status=200)
                    return JsonResponse({'message':'Bad String'}, status=400)
                return JsonResponse({'message':'Not Found'}, status=400)
            except(ObjectDoesNotExist)as e:
                return JsonResponse({'message':'Requested Document details Does Not Exist'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request):
        if request.data:
            try:
                document = EmployeeDocument.objects.get(id = request.data['id'])
                if document:
                    document.delete()
                    return JsonResponse({'message': 'Document Deleted Successfully'}, status=400)
                return JsonResponse({'message':'Not Found'}, status=400)
            except(ObjectDoesNotExist)as e:
                return JsonResponse({'message':'Request Document Does Not Exist'}, status=400)
        return JsonResponse({'message': 'Bad Request'}, status=400)


class EmployeeDocumentIndividual(APIView):
    def get(self, request, user):
        documents = EmployeeDocument.objects.filter(user=user)
        serializer = EmployeeDocumentSerializer(documents, many=True)
        return Response(serializer.data)

##############-------------------------HR Payrole----------------------####################


class HrUserListView(APIView):
    def get(self, request, format=None):
        if request.user.user_role.department == 'HR':
            employees = Role.objects.all()
            user_ids = [i.user_id for i in employees]
            users = User.objects.filter(id__in=user_ids)
            serializer = HrUserSerializer(users, many=True)
            return Response(serializer.data)
        return JsonResponse({'message':'Unauthorised user'}, status=401)

class HrUsersDetailsView(APIView):
    def get(self, request, user, format=None):
        print(user)
        if request.user.user_role.department == 'HR':
            user_obj = User.objects.filter(id=user)
            serializer = HrUserDetailSerializer(user_obj)
            print(serializer)
            return Response(serializer.data)
        return JsonResponse({'message':'Unauthorised user'}, status=401)
            

class SalaryView(APIView):
    def post(self, request, format=None):
        if request.data:
            serializer = SalarySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Saved Salary of the Employee'}, status=200)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        salary = Salary.objects.all()
        serializer = SalarySerializer(salary, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        if request.data:
            salary = Salary.objects.filter(user=request.data['user']).first()
            if salary:
                serializer = SalarySerializer(salary, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Updated Salary of the employee'}, status=200)
                return JsonResponse({'message':'Bad String'}, status=400)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(APIView):
        if request.data:
            salary = Salary.objects.filter(user=request.data['user']).first()
            if salary:
                salary.delete()
                return JsonResponse({'message':'Salary Deleted Successfully'}, status=200)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad String'}, status=400)


class SalaryIndividual(APIView):
    def get(self, request, user):
        salary = Salary.objects.get(user=user)
        serializer = SalarySerializer(salary)
        return Response(serializer.data)


############------------Bank Details-----------------################
class BankDetailsView(APIView):
    def post(self, request):
        if request.data:
            serializer = BankDetailsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Bank Details Of Employee Added Successfully'}, status=201)
            return JsonResponse({'message':'Bad String'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request):
        bankDetails = BankDetails.objects.all()
        serializer = BankDetailsSerializer(bankDetails, many=True)
        return Response(serializer.data)

    def put(self, request):
        if request.data:
            try:
                _id = request.data['id']
            except(KeyError)as e:
                return JsonResponse({'message':'Unique Id Required'}, status=400)
            bankDetails = BankDetails.objects.get(id=_id)
            serializer = BankDetailsSerializer(bankDetails, data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Bank Details Updated Successfully'}, status=200)
            return Response(serializer.errors)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request):
        if request.data:
            try:
                _id = request.data['id']
            except(KeyError)as e:
                return  JsonResponse({'message':'Unique Id Required'}, status=400)
            bankDetails = BankDetails.objects.get(id=_id)
            if bankDetails:
                bankDetails.delete()
                return JsonResponse({'message':'Bank Details Deleted Successfully'}, status=200)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

class BankDetailsIndividual(APIView):
    def get(self, request, user):
        bankDetails = BankDetails.objects.get(user = user)
        serializer = BankDetailsSerializer(bankDetails)
        return Response(serializer.data)





#############----------------Salary Request-------------##################
@api_view(['POST'])
def salary_request(request):
    user_id = request.data.get('user', None)
    month = request.data.get('month', None)
    year = request.data.get('year', None)
    if user_id:
        salary_info = Salary.objects.filter(user=user_id).first()
        calculate_lop = calculate_lop_f(user_id, month, year)
        salary_of_one_day = float(salary_info.net_salary)/float(25)
        lop_cost = float(calculate_lop)*float(salary_of_one_day)
        salary_request=SalaryRequest(
                user = salary_info.user,
                basic = salary_info.basic,
                hra = salary_info.hra,
                conveyance_allowance = salary_info.conveyance_allowance,
                deduction = lop_cost,
                misc_allowance = salary_info.misc_allowance,
                proffesional_tax = salary_info.proffesional_tax,
                net_salary = salary_info.net_salary
            )
        salary_request.save()
        return JsonResponse({'message':'Salary Requested'}, status=200)
    return JsonResponse({'message':'Bad Request'}, status=400)


def calculate_lop_f(user_id, month, year):
    employee_lop = EmployeeLop.objects.filter(user=user_id, appliedOn__month=month, appliedOn__year=year, status=True).all()
    print(employee_lop)
    lop = 0
    if employee_lop:
        for e in employee_lop:
            lop += e.count
            e.status=False
            e.save()
        return lop
    return lop

######----------Credit Salary--------######
class SalaryRequested(APIView):
    def get(self, request):
        salaries = SalaryRequest.objects.filter(credited=False).all()
        serializer = SalaryRequestedSerializer(salaries, many=True)
        return Response(serializer.data)

    def put(self, request):
        if request.data:
            _id = request.data.get('id', None)
            if _id:
                requested_salary = SalaryRequest.objects.filter(id=_id).first()
                serializer = SalaryRequestPutSerializer(requested_salary, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Requested Salary updated successfully'}, status=200)
                return Response(serializer.errors)
            return JsonResponse({'message':'Unique Id Required to identify requested salary'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)


#######--------Salary Credited--------##########
@api_view(['POST'])
def salary_credited(request):
    if request.data:
        _id = request.data.get('id', None)
        user_id = request.data.get('user', None)
        if _id and user_id:
            salary = SalaryRequest.objects.filter(id= _id, user=user_id, credited=False).first()
            if salary:
                salary.credited_on = timezone.localtime(timezone.now())
                salary.credited = True
                salary.save()
                return JsonResponse({'message':'Salary Request status changed to Creadited'}, status=200)
            return JsonResponse({'message':'Not Found, Invalid data'}, status=400)
        return JsonResponse({'message':'unique id and user id is neccessory'}, status=400)
    return JsonResponse({'message':'Bad Request'}, status=400)
