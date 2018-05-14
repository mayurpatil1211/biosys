from django.shortcuts import render
from .models import *
from .serializers import *

import os
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from annoying.functions import get_object_or_None
from datetime import date

import datetime
from collections import namedtuple
import time
from datetime import datetime, timedelta
from time import gmtime, strftime
import time
# Create your views here.
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from shutil import copyfile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
# from weasyprint import HTML

try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    @register_job(scheduler, "interval", seconds=10, replace_existing=True)
    def test_job():
        today = datetime.strftime(datetime.now(), "%Y-%m-%d")
        today=(datetime.strptime(today, '%Y-%m-%d')).date()
        tommorrow = today+timedelta(days=1)

        try:
            roomStatus = RoomStatus.objects.filter(status=True).all()

        except(KeyError, AttributeError, Exception)as e:
            roomStatus =[]
        if roomStatus:
            for room in roomStatus:
                if room.from_date<=today and today<=room.to_date:
                    try:
                        room.room.status = room.room_status
                        room.room.save()
                    except(KeyError, AttributeError, Exception)as e:
                        pass
                else:
                    try:
                        room.room.status= Status.Available
                        room.room.save()
                    except(KeyError, AttributeError, Exception)as e:
                        pass
        else:
            pass
    register_events(scheduler)
    scheduler.start()
except(TypeError)as e:
    pass



class RoomTypeView(APIView):
    def post(self, request, format=None):
        if request.data:
            serializers = RoomTypeSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return  JsonResponse({'message':'Room type saved Successfully'}, status=201)
            return Response(serializers.errors)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        roomTypes = RoomTypes.objects.all()
        serializers = RoomTypeSerializer(roomTypes, many=True)
        return Response(serializers.data)

    def put(self, request, format=None):
        if request.data:
            try:
                id = request.data['id']
            except(KeyError)as e:
                id = None

            roomType = RoomTypes.objects.filter(id = id).first()
            serializers = RoomTypeSerializer(roomType, data=request.data)
            if serializers.is_valid():
                serializers.save()
                return JsonResponse({'message':'Room type updated Successfully'}, status=200)
            return Response(serializers.errors)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request, format=None):
        if request.data:
            try:
                id = request.data['id']
            except(KeyError)as e:
                id= None

            roomType = RoomTypes.objects.filter(id = id).first()
            if roomType:
                roomType.delete()
                return JsonResponse({'message':'Room type deleted Successfully'}, status=200)
            return JsonResponse({'message':'Room type Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)


class RoomViewBasedDate(APIView):
    def post(self, request, format=None):
        from_date = request.data.get('from_date', None)
        to_date = request.data.get('to_date', None)
        
        from_date = (datetime.strptime(from_date, '%Y-%m-%d')).date()
        to_date = (datetime.strptime(to_date, '%Y-%m-%d')).date()
        rooms = Rooms.objects.all()
        rooms_status = []
        for roo in rooms:
            room = {}
            #  (room)
            room['id'] = roo.id
            room['room_number'] = roo.room_number
            room['floor'] = roo.floor
            room['current_status'] = str(roo.status)
            room['bookings']=[]
            bookings_obj = RoomStatus.objects.filter(room=roo, status=True).all()
            if bookings_obj:
                for book in bookings_obj:
                    booking = {}
                    if book.from_date <= from_date <=book.to_date and book.from_date<= to_date <=book.to_date:
                        booking['from_date'] = book.from_date
                        booking['to_date'] = book.to_date
                        booking['room_status'] = str(book.room_status)
                        booking['booking_item'] = {}
                        item = Booking.objects.filter(id=book.booking.id).first()
                        if item:
                            item_obj = {}
                            booking['booking_item']['id'] = item.id
                            booking['booking_item']['customer_first_name'] = item.customer_first_name
                            booking['booking_item']['customer_last_name'] = item.customer_last_name
                            booking['booking_item']['mobile_number'] = item.mobile_number
                            booking['booking_item']['email'] = item.email
                            booking['booking_item']['adults'] = item.adults
                            booking['booking_item']['child'] = item.child
                            booking['booking_item']['token_amount'] = item.token_amount
                            booking['booking_item']['check_out'] = item.check_out
                            booking['booking_item']['address'] = item.address
                            booking['booking_item']['city'] = item.city
                            booking['booking_item']['taluka'] = item.taluka
                            booking['booking_item']['pincode'] = item.pincode
                            # booking['booking_item'] = item_obj
                        else:
                            booking = {}
                        room['bookings'].append(booking)
                    else:
                        pass
            rooms_status.append(room)

        return JsonResponse({'rooms_status': rooms_status}, status=200)



class RoomStatusIndividualView(APIView):
    def put(self, request, format=None):
        if request.data:
            try:
                room = Rooms.objects.filter(id=request.data['id']).first()
            except(KeyError, AttributeError)as e:
                return JsonResponse({'message':'ID required'}, status=400)

            if room:
                serializers = RoomStatusSerializer(room, data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return JsonResponse({'message':'Room status changed Successfully'}, status=200)
                return Response(serializers.errors)
            return JsonResponse({'message':'Invalid Room'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

class RoomStatusMultipleView(APIView):
    def put(self, request, format=None):
        if request.data:
            for room in request.data:
                try:
                    room_instance = Rooms.objects.filter(id = room['id']).first()
                except(KeyError, AttributeError)as e:
                    room_instance = None
                    return JsonResponse({'message':'ID required'}, status=400)

                if room_instance:
                    serializers = RoomStatusSerializer(room_instance, data=room)
                    if serializers.is_valid():
                        serializers.save()
                    else:
                        return Response(serializers.errors)
                else:
                    pass
            return JsonResponse({'message':'Room status changed Successfully'}, status=200)
        return JsonResponse({'message':'Bad Request'}, status=400)

class RoomMaintenanceView(APIView):
    def put(self, request, id, format=None):
        room = Rooms.objects.filter(id=id).first()
        if room:
            if room.status != Status.Maintenance:
                room.status = Status.Maintenance
                room.save()
                return JsonResponse({'message':'Room under Maintenance'}, status=200)
            elif room.status == Status.Maintenance:
                room.status = Status.Available
                room.save()
                return JsonResponse({'message':'Room is Available Now'}, status=200)
            else:
                return JsonResponse({'message':'May be Room is Occupied Can\'t set status to Maintenance'}, status=400)
        return JsonResponse({'message':'Invalid Room'}, status=400)


class FoodCategoryView(APIView):
    def post(self, request, format=None):
        if request.data:
            serializers = FoodCategorySerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return JsonResponse({'message':'Food Category Added Successfully'}, status=201)
            return Response(serializers.errors)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        food_categories = FoodCategory.objects.all()
        serializers = FoodCategorySerializer(food_categories, many=True)
        return Response(serializers.data)

    def put(self, request, format=None):
        if request.data:
            food_category = FoodCategory.objects.filter(id=request.data['id']).first()
            if food_category:
                serializers = FoodCategorySerializer(food_category, data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return JsonResponse({'message':'Food Category updated Successfully'}, status=200)
                return Response(serializers.errors)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request, format=None):
        if request.data:
            food_category = FoodCategory.objects.filter(id=request.data['id']).first()
            if food_category:
                food_category.delete()
                return JsonResponse({'message':'Food Category Deleted Successfully'}, status=200)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)



class RoomView(APIView):
    def post(self, request, format=None):
        if request.data:
            try:
                serializers = RoomSerializer(data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return JsonResponse({'message':'Room Saved Successfully'}, status=200)
            except(KeyError)as e:
                return JsonResponse({'message':'Invalid status, Please Select Status From given List'}, status=400)
            return Response(serializers.errors)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        rooms = Rooms.objects.all()
        serializers = RoomGetSerializer(rooms, many=True)
        return Response(serializers.data)

    def put(self, request, format=None):
        if request.data:
            try:
                id = request.data['id']
            except(KeyError)as e:
                id = None
            room = Rooms.objects.filter(id = id).first()
            if room:
                serializers = RoomSerializer(room, data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return JsonResponse({'message':'Room details updated Successfully'}, status=200)
                return Response(serializers.errors)
            return JsonResponse({'message':'Room not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)


def check_room_availability(data):
    room_id = data.get('room', None)
    check_in = data.get('check_in', None)
    check_out = data.get('check_out', None)

    check_in = (datetime.strptime(check_in, '%Y-%m-%d')).date()
    check_out = (datetime.strptime(check_out, '%Y-%m-%d')).date()

    booking = Booking.objects.filter(room=room_id, status=True)
    for book in booking:
        if not book.check_in <= check_in <=book.check_out and not book.check_in<= check_out <=book.check_out:
            pass
        else:
            return 0
    return 1

class BookingView(APIView):
    def post(self, request, format=None):
        if request.data:
            try:
                room_id = request.data['room']
            except(KeyError)as e:
                room_id = None

            room = Rooms.objects.filter(id=room_id).first()
            if check_room_availability(request.data):
                if room:
                    serializers = BookingSerializer(data=request.data)
                    if serializers.is_valid():
                        serializers.save()
                        room.status = Status.Booked
                        room.save()
                        return JsonResponse({'message':'Room Booked Successfully'}, status=200)
                    return Response(serializers.errors)
                return JsonResponse({'message':'Sorry, Room Not Found'}, status=400)
            return JsonResponse({'message':'Sorry, Room is not Available on specified dates'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        bookings = Booking.objects.filter(status=True).all()
        serializers = BookingGetSerializer(bookings, many=True)
        return Response(serializers.data)

    def put(self, request, format=None):
        if request.data:
            try:
                booking_id = request.data['id']
            except(KeyError)as e:
                booking_id = None

            try:
                booking_instance = Booking.objects.get(id=booking_id)
            except(Exception) as e:
                return JsonResponse({'message':'Does Not Exist'}, status=400)

            if booking_instance:
                serializers = BookingSerializer(booking_instance, data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return JsonResponse({'message':'Booking Details Updated Successfully'}, status=200)
                return Response(serializers.errors)
            return JsonResponse({'message':'Invalid, Booking Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)


class CheckInAndBookView(APIView):
    def post(self, request, format=None):
        if request.data:
            try:
                room_id = request.data['room']
            except(KeyError)as e:
                room_id = None
            room = Rooms.objects.filter(id=room_id).first()
            availability = check_room_availability(request.data)
            if room:
                if availability:
                    if room.status == Status.Available:
                        serializers = CheckInBookingSerializer(data=request.data)
                        if serializers.is_valid():
                            serializers.save()
                            room.status = Status.Occupied
                            room.save()
                            return JsonResponse({'message':'Checked In Successfully'}, status=200)
                        return Response(serializers.errors)
                    return JsonResponse({'message':'Sorry, Room is '+ str(room.status) +' at this moment'}, status=400)
                return JsonResponse({'message':'Sorry, Room is not Available on specified dates'}, status=400)
            return JsonResponse({'message':'Sorry, Room Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        bookings = Booking.objects.filter(status=True, checked_in=True).all()
        serializers = BookingGetSerializer(bookings, many=True)
        return Response(serializers.data)

@api_view(['PUT'])
def check_in_booked_customer(request):
    if request.data:
        try:
            booking = Booking.objects.filter(id=request.data['booking_id'], checked_in=False).first()
        except(Exception) as e:
            return JsonResponse({'message':'Sorry this booking has already checked In'}, status=400)

        if booking:
            if booking.booking_status == Status.Occupied:
                return JsonResponse({'message':'Room already Occupied By another customer'}, status=400)
            else:
                booking.checked_in = True
                booking.room.status = Status.Occupied
                booking.booking_status = Status.Occupied
                room_obj = Rooms.objects.filter(id=booking.room.id).first()
                roomStatus_obj = RoomStatus.objects.filter(booking=booking).first()
                if room_obj:
                    room_obj.status = Status.Occupied
                    roomStatus_obj.room_status = Status.Occupied
                    booking.save()
                    room_obj.save()
                    roomStatus_obj.save()
                    return JsonResponse({'message':'Customer Checked In Successfully'}, status=200)
                return JsonResponse({'message':'Room Not Found'}, status=400)
        return JsonResponse({'message':'May be this booking has already checked in or not Available'}, status=400)


class AdditionalBillView(APIView):
    def post(self, request, format=None):
        if request.data:
            try:
                booking_id = request.data['booking']
            except(KeyError)as e:
                booking_id = None

            try:
                booking = Booking.objects.get(id=booking_id)
            except(Exception)as e:
                return JsonResponse({'message':'Invalid Booking'}, status=400)

            if booking:
                serializers = AdditionalBillSerializer(data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    return JsonResponse({'message':'Added bill of the Customer'}, status=200)
                return Response(serializers.errors)
            return JsonResponse({'message':'Not Found'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def put(self, request, format=None):
        if request.data:
            try:
                booking_id = request.data['booking']
            except(KeyError)as e:
                booking_id = None

            try:
                id = request.data['id']
            except(KeyError)as e:
                id = None

            if id:
                additional = AdditionalBill.objects.filter(id=id).first()
                if additional:
                    serializers = AdditionalBillSerializer(additional, data=request.data)
                    if serializers.is_valid():
                        serializers.save()
                        return JsonResponse({'message':'Customer Bill Updated'}, status=200)
                    return Response(serializers.errors)
                return JsonResponse({'message':'Not Found'}, status=400)
            return JsonResponse({'message': 'ID is reqired'}, status=400)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def delete(self, request, format=None):
        if request.data:
            for add in request.data:
                try:
                    id = add['id']
                except(KeyError)as e:
                    return JsonResponse({'message':'ID Required'}, status=400)

                try:
                    additional = AdditionalBill.objects.filter(id = id).first()
                except(Exception)as e:
                    return JsonResponse({'message':'Requested Bill Does Not Exist'}, status=400)

                if additional:
                    additional.delete()
            return JsonResponse({'message':'Requested Bill Deleted Successfully'}, status=200)
        return JsonResponse({'message':'Bad Request'}, status=400)

    def get(self, request, format=None):
        additional = AdditionalBill.objects.all()
        serializers = AdditionalBillSerializer(additional, many=True)
        return Response(serializers.data)

#-----CheckOut------

def change_roomStatus_on_checkout(booking):
    today = datetime.strftime(datetime.today().date(), '%Y-%m-%d')
    change_room_status = RoomStatus.objects.filter(booking=booking.id).first()
    if change_room_status:
        change_room_status.status = False
        change_room_status.room_status = Status.CheckedOut
        change_room_status.save()
    else:
        pass
    roomStatus = RoomStatus.objects.filter(room=booking.room, from_date=today, status=True).first()
    if roomStatus:
        roomStatus.room.status = roomStatus.room_status
        roomStatus.room.save()
        return 1
    change_room_status.room.status = Status.Available
    change_room_status.room.save()
    return 1


@api_view(['GET'])
def bookin_billing_info(request):
    main_obj = []                

    bookings = Booking.objects.filter(checked_in=True, booking_status=Status.Occupied).all()
    if bookings:
        for booking in bookings:
            if booking.check_out is None:
                booking.check_out = timezone.localtime(timezone.now())
            else:
                pass
            start_date = (booking.check_in).strftime("%Y-%m-%d")

            start_date1 = datetime.strptime(str(start_date), "%Y-%m-%d").date()

            today = datetime.strftime(datetime.now(), "%Y-%m-%d")
            today=(datetime.strptime(today, '%Y-%m-%d')).date()

            diff = abs((today-start_date1).days)

            booking.number_of_days = diff+1
            booking.save()
            final_bill = bill_on_checkout(booking.id)
            serializers = BookingBillingSerializer(booking)
            result = serializers.data
            main_obj.append(serializers.data)
            del_bill = Billing.objects.filter(booking=booking).first()
            del_bill.delete()
        return Response(main_obj)
    return JsonResponse({'message':'Either Invalid Booking or customer not checked in'}, status=400)




@api_view(['GET'])
@permission_classes((AllowAny,))
def bookin_billing_info_single(request, booking_id):
    booking = Booking.objects.filter(checked_in=True, id=booking_id).first()
    if booking:
        if booking.check_out is None:
            booking.check_out = timezone.localtime(timezone.now())
        else:
            pass
        start_date = (booking.check_in).strftime("%Y-%m-%d")

        start_date1 = datetime.strptime(str(start_date), "%Y-%m-%d").date()

        today = datetime.strftime(datetime.now(), "%Y-%m-%d")
        today=(datetime.strptime(today, '%Y-%m-%d')).date()

        diff = abs((today-start_date1).days)

        booking.number_of_days = diff+1
        booking.save()
        final_bill = bill_on_checkout(booking.id)
        serializers = BookingBillingSerializer(booking)
        result = serializers.data
        del_bill = Billing.objects.filter(booking=booking).first()
        del_bill.delete()
        return Response(result)
    return JsonResponse({'message':'Either Invalid Booking or customer not checked in'}, status=400)

@api_view(['POST'])
def check_out(request):
    if request.data:                
        try:
            booking_id = request.data['booking']
        except(KeyError)as e:
            return JsonResponse({'message':'Please Tell Us which booking'}, status=400)

        booking = Booking.objects.filter(id=booking_id, checked_in=True).first()
        if booking:
            if booking.check_out is None:
                today = datetime.strftime(datetime.now(), "%Y-%m-%d")
                booking.check_out = (datetime.strptime(today, '%Y-%m-%d')).date()
            else:
                pass
            booking.status=False #checkout flag
            booking.booking_status = Status.CheckedOut
            change_roomStatus_on_checkout(booking)
            # start_date = (booking.check_in).strftime("%Y-%m-%d")
            # end_date = (booking.check_out).strftime("%Y-%m-%d")
            # start_date1 = datetime.strptime(str(start_date), "%Y-%m-%d")
            # end_date1 = datetime.strptime(str(end_date), "%Y-%m-%d")
            # diff = abs((end_date1-start_date1).days)
            # booking.number_of_days = diff+1
            # booking.save()

            start_date = (booking.check_in).strftime("%Y-%m-%d")

            start_date1 = datetime.strptime(str(start_date), "%Y-%m-%d").date()

            today = datetime.strftime(datetime.now(), "%Y-%m-%d")
            today=(datetime.strptime(today, '%Y-%m-%d')).date()
            booking.check_out = today
            roomStatus = RoomStatus.objects.filter(booking=booking).first()
            roomStatus.to_date = today
            roomStatus.save()
            diff = abs((today-start_date1).days)
            booking.number_of_days = diff+1
            booking.save()

            final_bill = bill_on_checkout(booking.id)
            serializers = BookingBillingSerializer(booking)
            return Response(serializers.data)
        return JsonResponse({'message':'Either Invalid Booking or customer not checked in'}, status=400)
    return JsonResponse({'message':'Bad Request'}, status=400)

def bill_on_checkout(booking_id):
    booking = Booking.objects.filter(id=booking_id).first()
    if booking:
        additional_bill = calculate_additional_bill(booking.id)
        room = Rooms.objects.filter(id = booking.room.id).first()
        room_price = room.room_type.price
        tax = room.room_type.tax

        add_bill = Billing(
            booking = booking,
            additional_amount = additional_bill,
            room_price = room_price,
            tax = tax,
            number_of_days = booking.number_of_days
            )
        add_bill.save()
        return 1
    return 0

def calculate_additional_bill(booking_id):
    add_bill = AdditionalBill.objects.filter(booking=booking_id).all()
    total = 0
    for bill in add_bill:
        total += bill.total
    return total


#-----CheckOut Ends-------

class BookingInfo(APIView):
    def get(self, request, booking_id):
        booking = Booking.objects.get(id=booking_id)
        serializers = BookingInfoSerializer(booking, many=False)
        return Response(serializers.data)


class BookingHistory(APIView):
    def get(self, request, format=None):
        booking = Booking.objects.filter(status=False)
        serializers = BookingInfoSerializer(booking, many=True)
        return Response(serializers.data)

class BookingHistoryFilter(APIView):
    def post(self, request,format=None):
        if request.data:
            result = []
            try:
                name = request.data['customer_name']
            except(KeyError)as e:
                name = None

            try:
                date = request.data['date']
            except(KeyError)as e:
                date = None

            if name:
                booking = Booking.objects.filter(status=False, customer_name__icontains=name).all()
                serializers = BookingInfoSerializer(booking, many=True)
                result.extend(serializers.data)

            if date:
                booking = Booking.objects.filter(status=False, check_in__icontains=date, check_out__icontains=date).all()
                serializers = BookingInfoSerializer(booking, many=True)
                result.extend(serializers.data)
            return Response(result)
        return JsonResponse({'message':'Bad Request'}, status=400)



class RoomHistoryView(APIView):
    def post(self, request, room_id, format=None):
        from_date = request.data.get('from_date', None)
        to_date = request.data.get('to_date', None)
        check_in = (datetime.strptime(from_date, '%Y-%m-%d')).date()
        check_out = (datetime.strptime(to_date, '%Y-%m-%d')).date()
        # booking = RoomStatus.objects.filter(Q(from_date__gte=check_in) | Q(to_date__lte=check_out)).filter(room=room_id, status=True)
        booking = RoomStatus.objects.filter(Q(from_date__range=[check_in, check_out]) | Q(to_date__range=[check_in, check_out])).filter(room=room_id)
        serializers = RoomStatusSerializer(booking, many=True)
        return Response(serializers.data)

class RoomHistoryAll(APIView):
    def post(self, request, format=None):
        from_date = request.data.get('from_date', None)
        to_date = request.data.get('to_date', None)
        check_in = (datetime.strptime(from_date, '%Y-%m-%d')).date()
        check_out = (datetime.strptime(to_date, '%Y-%m-%d')).date()

        booking = RoomStatus.objects.filter(Q(from_date__range=[check_in, check_out]) | Q(to_date__range=[check_in, check_out]))
        serializers = RoomStatusSerializer(booking, many=True)
        return Response(serializers.data)

##################--Cancel Booking--#################
@api_view(['PUT'])
def cancel_booking(request):
    id = request.data.get('booking_id', None)
    if id:
        booking = Booking.objects.filter(id=id).first()
        if booking:
            booking.status=False
            roomStatus = RoomStatus.objects.filter(booking=id).first()
            roomStatus.status = False
            booking.save() 
            roomStatus.save()
            room = Rooms.objects.filter(id=booking.room.id).first()
            room.status=Status.Available
            room.save()
            return JsonResponse({'message':'Booking Canceled Successfully'}, status=200)
        return JsonResponse({'message':'Invalid Booking'}, status=400)
    return JsonResponse({'message':'Bad Request'}, status=400)

    ###############---Generate PDF----############
from django.http import HttpResponse
from django.template.loader import get_template
from dscignBiosys.utils import render_to_pdf #created in step 4

@api_view(['GET'])
@permission_classes((AllowAny,))
def generate_pdf(request, *args, **kwargs):
    template = get_template('invoice.html')
    data = {
            "id": 24,
            "room": {
                "room_number": "102",
                "floor": 3,
                "room_type": {
                "id": 1,
                "room_type": "Delux AC",
                "price": 1000,
                "tax": 11.2,
                "description": 'null',
                "updated_on": "2018-01-18T13:02:12.433119+05:30"
                }
            },
            "customer_first_name": "Johny",
            "customer_last_name": "mendola",
            "adults": 1,
            "check_in": "2018-02-23",
            "check_out": "2018-02-27",
            "child": 0,
            "address": "USA",
            "city":"banglore",
            "phone_number":"+919019802163",
            "email": "john@gmail.com",
            "id_proof_one": 'null',
            "id_proof_two": 'null',
            "taluka": "CA",
            "checked_in": 'true',
            "booking_status": "CheckedOut",
            "token_amount": 500,
            "pincode": 590014,
            "additional_bill": [],
            "booking_bill": {
                "id": 26,
                "paid_by": "Cash",
                "additional_amount": 0,
                "room_price": 1000,
                "tax": 11.2,
                "number_of_days": 5,
                "total_amount": 5060,
                "booking": 24
            }
            }
    # html = template.render(data)
    pdf = render_to_pdf('invoice.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
    # return HttpResponse(html)