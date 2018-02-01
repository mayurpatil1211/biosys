import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
import uuid
import datetime



@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class RoleTypes(models.Model):
    role_type = models.CharField(max_length=20)


class Role(models.Model):
    user = models.OneToOneField(User, related_name='user_role', on_delete=models.CASCADE)
    role_type = models.CharField(max_length=20)
    department = models.CharField(max_length=20)




class Employees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_other_details')
    phone_no = models.CharField(max_length=13, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.IntegerField(null=True)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    mother_name = models.CharField(max_length=50, null=True, blank=True)
    pan_card = models.CharField(max_length=100,  null=True, blank=True)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    approved_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name




class EmployeeDocument(models.Model):
    user = models.ForeignKey(User, related_name='user_document', on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100, null=True, blank=True)
    ducument_file = models.FileField(null=True, blank=True)
    document_description = models.CharField(max_length=200, null=True, blank=True)
    file_type = models.CharField(max_length=20, null=True, blank=True)
    verified = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user+' '+self.document_name


class Department(models.Model):
    name = models.CharField(max_length=20)

class Attendance(models.Model):
    user = models.ForeignKey(User, related_name='user_attendance', on_delete=models.CASCADE)
    clock_in = models.DateTimeField(null=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)


class Activity(models.Model):
    name = models.CharField(max_length=200)
    activity_date = models.DateField(null=True,blank=True)
    description = models.CharField(max_length=200, null=True,blank=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    status = models.CharField(max_length=20, null=True,blank=True)
    created_by = models.ForeignKey(User, related_name='user_activity', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


class Expense(models.Model):
    activity = models.ForeignKey(Activity, related_name='activity', on_delete=models.SET_NULL, null=True,blank=True)
    reason = models.CharField(max_length=100, null=True,blank=True)
    description = models.CharField(max_length=500, null=True,blank=True)
    amount = models.IntegerField(null=True,blank=True)
    expense_type = models.CharField(max_length=100, null=True,blank=True)
    created_by = models.ForeignKey(User, related_name='user_expense', on_delete=models.CASCADE)
    aproved_by = models.ForeignKey(User, related_name='aproved_expense', on_delete=models.SET_NULL, null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    status = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    approvedOn = models.DateField(auto_now_add=True)
    actionOn = models.DateField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.id



class Holiday(models.Model):
    date = models.DateField(null=False)
    reason = models.CharField(max_length=500, null=True,blank=True)

    def __str__(self):
        return self.reason


class Leaves(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance_sick_leave = models.FloatField()
    total_sick_leave = models.FloatField()
    balance_casual_leave = models.FloatField()
    total_casual_leave = models.FloatField()
    balance_earned_leave = models.FloatField()
    total_earned_leave = models.FloatField()
    balance_compoff_leave = models.FloatField()
    total_compoff_leave = models.FloatField()
    total_lop = models.FloatField(default=0)

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name

class EmployeeLop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appliedOn = models.DateField(auto_now_add=True)
    count = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name


class AppliedLeave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type_of_leave = models.CharField(max_length=100)
    leave_from = models.DateField(null=True,blank=True)
    to_leave = models.DateField(null=True,blank=True)
    number_of_days = models.FloatField(max_length=5)
    reason = models.CharField(max_length=200, null=True,blank=True)
    status = models.BooleanField(default=False)
    appliedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_leave')
    approvedBy = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='approved_by',blank=True)
    appliedOn = models.DateField(auto_now_add=True, null=False)
    actionOn = models.DateTimeField(null=True,blank=True)
    declined = models.BooleanField(default=False)
    # end_date-start_date

    def save(self, *args, **kwarg):
        start_date = datetime.datetime.strptime(str(self.leave_from), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(str(self.to_leave), "%Y-%m-%d")
        diff = abs((end_date-start_date).days)
        print(diff)
        self.number_of_days = diff
        super(AppliedLeave, self).save(*args, **kwarg)

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name



########################-------------Form 1----------------###############################
class FarmerDetails(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.SET_NULL, related_name="activity_farmer", null=True,blank=True)
    farmer_name = models.CharField(max_length=100, null=True,blank=True)
    state = models.CharField(max_length=100, null=True,blank=True)
    district = models.CharField(max_length=100, null=True,blank=True)
    taluka = models.CharField(max_length=100, null=True,blank=True)
    address = models.CharField(max_length=500, null=True,blank=True)
    pin = models.CharField(max_length=10, null=True,blank=True)
    longitude = models.CharField(max_length=50, null=True,blank=True)
    latitude = models.CharField(max_length=50, null=True,blank=True)
    primary_phone = models.CharField(max_length=15, null=True,blank=True)
    secondary_phone = models.CharField(max_length=15, null=True,blank=True)
    email = models.EmailField(max_length=200, null=True,blank=True)
    land_area = models.CharField(max_length=500, null=True,blank=True)
    soil_color = models.CharField(max_length=200, null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    form_filled_on = models.DateField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.farmer_name


class FarmerSoilType(models.Model):
	farmer = models.ForeignKey(FarmerDetails, null=False, on_delete=models.CASCADE, related_name='soil_type')
	soil = models.CharField(max_length=100, null=True,blank=True)

	def __str__(self):
		return self.farmer.farmer_name


class FarmerCropType(models.Model):
	farmer = models.ForeignKey(FarmerDetails, null=False, on_delete=models.CASCADE, related_name='crop_type')
	crop = models.CharField(max_length=100, null=True,blank=True)

	def __str__(self):
		return self.farmer.farmer_name


#######################----------------Form 2---------------#################################

class CultivationForm(models.Model):
    farmer = models.ForeignKey(FarmerDetails, on_delete=models.CASCADE, related_name="farmer_cultivation")
    previous_year = models.DateField(null=True,blank=True)
    crop_details = models.CharField(max_length=200, null=True,blank=True)
    crop_type = models.CharField(max_length=50, null=True,blank=True)
    pesticides = models.CharField(max_length=100, null=True,blank=True)
    deases = models.CharField(max_length=100, null=True,blank=True)
    chemicals = models.CharField(max_length=100, null=True,blank=True)
    fertilizer = models.CharField(max_length=200, null=True,blank=True)
    soil_test_report = models.CharField(max_length=1000, null=True,blank=True)
    water_test_report = models.CharField(max_length=1000, null=True,blank=True)

    def __str__(self):
        return self.farmer.farmer_name

##############--------------Sample Form---------------#######################

class SampleForm(models.Model):
    farmer = models.ForeignKey(FarmerDetails, on_delete=models.CASCADE, related_name="farmer_sample")
    sample = models.CharField(max_length=200, null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    previous_year = models.DateField(null=True,blank=True)
    sample_request = models.CharField(max_length=200, null=True,blank=True)
    sample_request_qauntity = models.IntegerField(null=True,blank=True)
    sample_given_date = models.DateField(auto_now_add=True, null=True,blank=True)
    photo_upload = models.CharField(max_length=1000, null=True,blank=True)
    excepted_result_date = models.DateField(null=True,blank=True)
    excepted_result_photo = models.CharField(max_length=1000, null=True,blank=True)
    excepted_result_note = models.CharField(max_length=500, null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True,blank=True)

    def __str__(self):
        return self.farmer.farmer_name

#################--------------DealerApplicationForm---------###############

class DealerForm(models.Model):
    branch_name = models.CharField(max_length=200, null=True,blank=True)
    firm_name = models.CharField(max_length=200, null=True,blank=True)
    address = models.CharField(max_length=500, null=True,blank=True)
    safety_deposit_ammount= models.FloatField(null=True,blank=True)
    distributor_bank_account_number = models.CharField(max_length=30, null=True,blank=True)
    distributor_bank_name = models.CharField(max_length=100, null=True,blank=True)
    ifsc_or_rtgs = models.CharField(max_length=100, null=True,blank=True)
    branch_contact_number = models.CharField(max_length=15, null=True,blank=True)
    tin_number = models.CharField(max_length=100, null=True,blank=True)
    safety_check_one = models.CharField(max_length=100, null=True,blank=True)
    safety_check_two = models.CharField(max_length=100, null=True,blank=True)
    firm_status = models.CharField(max_length=20, null=True,blank=True)
    dealer_name = models.CharField(max_length=100, null=True,blank=True)
    dealer_father_name = models.CharField(max_length=50, null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    dealer_address = models.CharField(max_length=500, null=True,blank=True)
    dealer_phone_number = models.CharField(max_length=15, null=True,blank=True)
    heir_guarantor = models.CharField(max_length=50, null=True,blank=True)

    def __str__(self):
        return self.branch_name+', '+self.dealer_name

#############################---------Orders--------##########################

class Items(models.Model):
    item_name = models.CharField(max_length=100, null=True,blank=True)
    item_code = models.CharField(max_length=100, null=True,blank=True)
    hsn_sac_code = models.CharField(max_length=200, null=True,blank=True)
    description = models.CharField(max_length=1000, null=True,blank=True)
    uom = models.CharField(max_length=200, null=True,blank=True)
    rate = models.FloatField(null=True,blank=True)
    discount_amount = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.item_name


class VendorType(models.Model):
    vendor_type = models.CharField(max_length=100)

class Vendors(models.Model):
    vendor_name = models.CharField(max_length=200, null=True,blank=True)
    vendor_address = models.CharField(max_length=500, null=True,blank=True)
    vendor_city = models.CharField(max_length=50, null=True,blank=True)
    vendor_pin_code = models.IntegerField(null=True,blank=True)
    vendor_pan = models.CharField(max_length=50, null=True,blank=True)
    vendor_gst = models.CharField(max_length=100, null=True,blank=True)
    vendor_contact = models.IntegerField(null=True,blank=True)
    vendor_type = models.CharField(max_length=100, null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.vendor_name


# class Orders(models.Model):
#     vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, related_name="vendor_order")
#     item_code = models.CharField(max_length=500)
#     hsn_sac_code = models.CharField(max_length=200)
#     item_name = models.CharField(max_length=500)
#     description = models.CharField(max_length=1000)
#     uom = models.CharField(max_length=200)
#     qty = models.FloatField()
#     rate = models.FloatField()
#     discount_amount = models.FloatField()
#     total_amount = models.FloatField()

#     def __str__(self):
#         return self.item_code+' '+self.item_name

class Orders(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, related_name="vendor_order")
    po = models.CharField(max_length=100, null=True,blank=True)
    shipping_address = models.CharField(max_length=1000, null=True,blank=True)
    discount_amount = models.FloatField(null=True,blank=True)
    total_amount = models.FloatField(null=True,blank=True)
    comfirmed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    po_date = models.DateTimeField(auto_now_add=True)

    # def __init__(self):
    #     super(Orders, self).__init__()
    #     self.po = str(uuid.uuid4())

    # def __str__(self):
    #     return self.str(id)
        

class ShippingAddress(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, related_name="vendor_shipping_address")
    address = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.vendor.vendor_name+' '+self.address

class OrderedItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="order_items")
    item_code = models.CharField(max_length=200, null=True,blank=True)
    hsn_sac_code = models.CharField(max_length=200, null=True,blank=True)
    item_name = models.CharField(max_length=500, null=True,blank=True)
    description = models.CharField(max_length=1000, null=True,blank=True)
    uom = models.CharField(max_length=200, null=True,blank=True)
    qty = models.FloatField(null=True,blank=True)
    discount_amount = models.FloatField(null=True,blank=True)
    rate = models.FloatField(null=True,blank=True)
    total_amount = models.FloatField(null=True,blank=True)

    @property
    def calculate_bill(self):
        quantity = self.qty
        price = self.rate
        discount = self.discount_amount

        actual_amount = float(quantity) * float(price)
        one_percent_discount = float(actual_amount)/100
        calculate_discount = float(one_percent_discount) * discount
        final_amount = float(actual_amount)-float(calculate_discount) 
        return final_amount


    def save(self, *args, **kwarg):
        self.total_amount = self.calculate_bill
        super(OrderedItems, self).save(*args, **kwarg)

    def __str__(self):
        return self.item_code+' '+self.item_name


#####------------------HR Payrole------------------#####

class BankDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_bank')
    bank_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=50)
    account_type = models.CharField(max_length=20)
    bank_address = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=13, null=True, blank=True)
    bmicr_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.first_name+' '+self.bank_name


class Salary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_salary')
    basic = models.FloatField()
    hra = models.FloatField()
    conveyance_allowance = models.FloatField(null=True)
    misc_allowance = models.FloatField(null=True)
    proffesional_tax = models.FloatField(null=True)
    net_salary = models.FloatField(null=True)
    net_salary_anum = models.FloatField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def calculate_net_salary(self):
        calculate_salary = self.basic+self.hra+self.conveyance_allowance+self.misc_allowance
        tax = (calculate_salary/100)*self.proffesional_tax
        net_salary = calculate_salary - tax
        return net_salary

    @property
    def calculate_net_salary_anum(self):
        net_salary_anum = self.net_salary * 12
        return net_salary_anum

    def save(self, *args, **kwarg):
        self.net_salary = self.calculate_net_salary
        self.net_salary_anum = self.calculate_net_salary_anum
        super(Salary, self).save(*args, **kwarg)

class SalaryRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salaries')
    basic = models.FloatField(null=True)
    hra = models.FloatField(null=True)
    conveyance_allowance = models.FloatField(null=True)
    deduction = models.FloatField(null=True)
    misc_allowance = models.FloatField(null=True)
    proffesional_tax = models.FloatField(null=True)
    net_salary = models.FloatField(null=True)
    net_salary_paybale = models.FloatField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    credited = models.BooleanField(default=False)
    credited_on = models.DateTimeField(null=True)

    # @property
    # def calculate_net_salary(self):
    #     calculate_salary = self.basic+self.hra+self.conveyance_allowance+self.misc_allowance
    #     tax = (basic_salary/100)*self.proffesional_tax
    #     net_salary = calculate_salary - tax
    #     return net_salary

    # @property
    # def calculate_deduction(self):
    #     deduction = self.net_salary - self.deduction
    #     return deduction

    def save(self, *args, **kwarg):
        # self.net_salary = self.calculate_net_salary
        # self.deduction = self.calculate_deduction
        self.net_salary_paybale = self.net_salary-self.deduction
        super(SalaryRequest, self).save(*args, **kwarg)

