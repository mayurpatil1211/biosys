from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.conf import settings
from collections import namedtuple

# Timeline = namedtuple('Timeline', ('tweets', 'articles'))


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):
    user_role = RoleSerializer()

    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'email', 'user_role')

class ActivityFarmerIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerDetails
        fields = ['id']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format="%H:%M", required=False)
    end_time = serializers.TimeField(format="%H:%M", required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)
    activity_date = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Activity
        fields = '__all__'


class ActivityFarmerMobSerializer(serializers.ModelSerializer):
    activity_farmer = ActivityFarmerIdSerializer(many=False, required=False)
    start_time = serializers.TimeField(format="%H:%M", required=False)
    end_time = serializers.TimeField(format="%H:%M", required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)
    activity_date = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Activity
        fields = [
                    'id',
                    'name',
                    'activity_date',
                    'description',
                    'start_time',
                    'end_time',
                    'status',
                    'created_by',
                    'created_on',
                    'activity_farmer'
                    ]


###############Employee Document################
class EmployeeDocumentSerializer(serializers.ModelSerializer):
    document_name = serializers.CharField(required=False, allow_blank=True)
    document_description = serializers.CharField(required=False, allow_blank=True)
    file_type = serializers.CharField(required=False, allow_blank=True)
    verified = serializers.BooleanField(required=False)

    class Meta:
        model = EmployeeDocument
        fields = '__all__'


################Employee Document Ends###############


class UpadteActivitySerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(format="%H:%M", required=False)
    end_time = serializers.TimeField(format="%H:%M", required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)
    activity_date = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Activity
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    reason = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    amount = serializers.IntegerField(required=False)
    expense_type = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateField(required=False)
    actionOn = serializers.DateField(required=False)

    class Meta:
        model = Expense
        fields = '__all__'

class EmployeesExpenseForManager(serializers.ModelSerializer):
    user_role = RoleSerializer()
    user_expense = ExpenseSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'user_role', 'user_expense')



"""leave management"""

  # user = models.ForeignKey(User, on_delete=models.CASCADE)
  #   type_of_leave = models.CharField(max_length=100)
  #   leave_from = models.DateField(null=True,blank=True)
  #   to_leave = models.DateField(null=True,blank=True)
  #   number_of_days = models.FloatField(max_length=5)
  #   reason = models.CharField(max_length=200, null=True,blank=True)
  #   status = models.BooleanField(default=False)
  #   appliedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_leave')
  #   approvedBy = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='approved_by',blank=True)
  #   appliedOn = models.DateField(auto_now_add=True, null=False)
  #   actionOn = models.DateTimeField(null=True,blank=True)
  #   declined = models.BooleanField(default=False)


class AppliedLeaveListSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False)
    appliedOn = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)

    class Meta:
        model = AppliedLeave
        fields = ['id', 'user', 'type_of_leave', 'leave_from', 'to_leave', 'number_of_days', 'reason', 'appliedOn','status','actionOn', 'declined']


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'


class AppliedLeaveSerializer(serializers.ModelSerializer):
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    appliedOn = serializers.DateField(required=False)
    appliedBy = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)
    status = serializers.BooleanField(required=False)
    
    class Meta:
        model = AppliedLeave
        fields = '__all__'

class ApplyLeaveSerializer(serializers.ModelSerializer):
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    appliedOn = serializers.DateField(required=False)
    appliedBy = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)
    status = serializers.BooleanField(required=False)
    
    class Meta:
        model = AppliedLeave
        fields = '__all__'
# reason
# status
# appliedBy
# approvedBy
# appliedOn
# actionOn
# declined

# ('id', 'user', 'type_of_leave', 'leave_from', 'to_leave', 'number_of_days', 'reason', 'appliedOn', 'declined', 'actionOn')


class LeavesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Leaves
        fields = [
                    'id', 
                    'balance_sick_leave', 
                    'total_sick_leave',
                    'balance_casual_leave',
                    'total_casual_leave',
                    'balance_earned_leave',
                    'total_earned_leave',
                    'balance_compoff_leave',
                    'total_compoff_leave',
                    'user'
                    ]


class BalanceLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ('id', 'balance_sick_leave', 'total_sick_leave', 'balance_casual_leave', 'total_casual_leave', 'balance_earned_leave', 'total_earned_leave', 'balance_compoff_leave', 'total_compoff_leave')


# class ManagerLeaveViewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AppliedLeave
#         fields = '__all__'

class ManagerLeaveViewSerializer(serializers.ModelSerializer):
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    appliedOn = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)
    class Meta:
        model = AppliedLeave
        # fields = ('id', 'type_of_leave', 'leave_from', 'to_leave', 'number_of_days', 'appliedOn')
        fields = [
            'id',
            'type_of_leave',
            'leave_from',
            'to_leave',
            'number_of_days',
            'status',
            'appliedOn',
            'approvedBy',
            'actionOn',
            'reason',
            'declined'
            ]


class AppliedLeaveHistory(serializers.ModelSerializer):
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    appliedOn = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)
    class Meta:
        model = AppliedLeave
        fields = '__all__'

class AppliedLeaveUpdate(serializers.ModelSerializer):
    type_of_leave = serializers.CharField(required=False, allow_blank=True)
    leave_from = serializers.DateField(required=False)
    to_leave = serializers.DateField(required=False)
    number_of_days = serializers.FloatField(required=False)
    reason = serializers.CharField(required=False, allow_blank=True)
    appliedOn = serializers.DateField(required=False)
    actionOn = serializers.DateTimeField(required=False)
    declined = serializers.BooleanField(required=False)
    class Meta:
        model = AppliedLeave
        fields = ('id', 'user', 'type_of_leave', 'leave_from', 'to_leave', 'number_of_days', 'reason', 'appliedOn', 'actionOn', 'declined')

        
class EmployeesLeaveForManager(serializers.ModelSerializer):
    user_role = RoleSerializer()
    users_leave = ManagerLeaveViewSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'user_role', 'users_leave')

#####---Leave Ends------############


class FarmerSoilTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerSoilType
        fields = ('id', 'farmer', 'soil')


class FarmerCropTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerCropType
        fields = ('id', 'farmer', 'crop')


class UpdateFarmerDetails(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    farmer_name = serializers.CharField(required=True, allow_blank=True)
    state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    district = serializers.CharField(max_length=100,required=False, allow_blank=True)
    taluka = serializers.CharField(max_length=100,required=False, allow_blank=True)
    address = serializers.CharField(max_length=500, required=False, allow_blank=True)
    pin = serializers.CharField(max_length=10, required=False, allow_blank=True)
    longitude = serializers.CharField(max_length=50, required=False, allow_blank=True)
    latitude = serializers.CharField(max_length=50, required=False, allow_blank=True)
    primary_phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    secondary_phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    email = serializers.EmailField(max_length=200, required=False, allow_blank=True)
    land_area = serializers.CharField(max_length=500,required=False, allow_blank=True)
    soil_color = serializers.CharField(max_length=200, required=False, allow_blank=True)

    class Meta:
        model = FarmerDetails
        fields = (
                    'id',
                    'farmer_name', 
                    'state', 
                    'district', 
                    'taluka', 
                    'address', 
                    'pin', 
                    'longitude', 
                    'latitude', 
                    'primary_phone', 
                    'secondary_phone', 
                    'email',
                    'land_area', 
                    'soil_color',
                    )
                  

    def update(self, instance, validated_data):
        soils = validated_data.pop('soil_type')
        crops = validated_data.pop('crop_type')
        instance.farmer_name = validated_data.get('farmer_name', instance.farmer_name)
        instance.state = validated_data.get('state', instance.state)
        instance.district = validated_data.get('district', instance.district)
        instance.taluka = validated_data.get('taluka', instance.taluka)
        instance.address = validated_data.get('address', instance.address)
        instance.pin = validated_data.get('pin', instance.pin)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.primary_phone = validated_data.get('primary_phone', instance.primary_phone)
        instance.secondary_phone = validated_data.get('secondary_phone', instance.secondary_phone)
        instance.email = validated_data.get('email', instance.email)
        instance.land_area = validated_data.get('land_area', instance.land_area)
        instance.soil_color = validated_data.get('soil_color', instance.soil_color)

        instance.save()

        soils = validated_data.get('soil_type')

        crops = validated_data.get('crop_type')

        if soils:
            for item in soils:
                item_id = item.get('id', None)
                if item_id:
                    soil_type = FarmerSoilType.objects.get(id=item_id)
                    soil_type.soil = item.get('soil', soil_type.soil)
                    soil_type.save()
                else:
                    FarmerSoilType.objects.create(farmer=instance, **item)

        if crops:
            for item in crops:
                item_id = item.get('id', None)
                if item_id:
                    crop_type = FarmerCropType.objects.get(id=item_id)
                    crop_type.soil = item.get('soil', crop_type.soil)
                    crop_type.save()
                else:
                    FarmerCropType.objects.create(farmer=instance, **item)
        return instance


class FarmerDetailsSerializer(serializers.ModelSerializer):
    # form_filled_on = serializers.DateField(format=settings.DATE_INPUT_FORMATS, input_formats=settings.DATE_INPUT_FORMATS)
    soil_type = FarmerSoilTypeSerializer(many=True)
    crop_type = FarmerCropTypeSerializer(many=True)
    farmer_name = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    district = serializers.CharField(required=False, allow_blank=True)
    taluka = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    pin = serializers.CharField(required=False, allow_blank=True)
    longitude = serializers.CharField(required=False, allow_blank=True)
    latitude = serializers.CharField(required=False, allow_blank=True)
    primary_phone = serializers.CharField(required=False, allow_blank=True)
    secondary_phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    land_area = serializers.CharField(required=False, allow_blank=True)
    soil_color = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model= FarmerDetails
        fields = [
                    'id',
                    'activity',
                    'created_by',
                    'farmer_name', 
                    'state', 
                    'district', 
                    'taluka', 
                    'address', 
                    'pin', 
                    'longitude', 
                    'latitude', 
                    'primary_phone', 
                    'secondary_phone', 
                    'email', 
                    'form_filled_on',
                    'land_area', 
                    'soil_color', 
                    'soil_type', 
                    'crop_type'
                ]


class CultivationFormSerializer(serializers.ModelSerializer):
    previous_year = serializers.DateField(format=settings.DATE_INPUT_FORMATS, input_formats=settings.DATE_INPUT_FORMATS, required=False)
    crop_details = serializers.CharField(allow_blank=True, required=False)
    crop_type = serializers.CharField(allow_blank=True, required=False)
    pesticides = serializers.CharField(allow_blank=True, required=False)
    deases = serializers.CharField(allow_blank=True, required=False)
    chemicals = serializers.CharField(allow_blank=True, required=False)
    fertilizer = serializers.CharField(allow_blank=True, required=False)
    soil_test_report = serializers.CharField(allow_blank=True, required=False)
    water_test_report = serializers.CharField(allow_blank=True, required=False)
    class Meta:
        model = CultivationForm
        fields = [
            'id',
            'farmer',
            'previous_year',
            'crop_details',
            'crop_type',
            'pesticides',
            'deases',
            'chemicals',
            'fertilizer',
            'soil_test_report',
            'water_test_report',
        ]



class CultivationAndFarmerDetails(serializers.ModelSerializer):
    farmer_name = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    district = serializers.CharField(required=False, allow_blank=True)
    taluka = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    pin = serializers.CharField(required=False, allow_blank=True)
    longitude = serializers.CharField(required=False, allow_blank=True)
    latitude = serializers.CharField(required=False, allow_blank=True)
    primary_phone = serializers.CharField(required=False, allow_blank=True)
    secondary_phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    land_area = serializers.CharField(required=False, allow_blank=True)
    soil_color = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = FarmerDetails
        fields=('id', 'farmer_name')

class CultivationFormReadSerializer(serializers.ModelSerializer):
    previous_year = serializers.DateField(required=False)
    crop_details = serializers.CharField(allow_blank=True, required=False)
    crop_type = serializers.CharField(allow_blank=True, required=False)
    pesticides = serializers.CharField(allow_blank=True, required=False)
    deases = serializers.CharField(allow_blank=True, required=False)
    chemicals = serializers.CharField(allow_blank=True, required=False)
    fertilizer = serializers.CharField(allow_blank=True, required=False)
    soil_test_report = serializers.CharField(allow_blank=True, required=False)
    water_test_report = serializers.CharField(allow_blank=True, required=False)
    class Meta:
        model = CultivationForm
        fields = (
            'id',
            'farmer',
            'previous_year',
            'crop_details',
            'crop_type',
            'pesticides',
            'deases',
            'chemicals',
            'fertilizer',
            'soil_test_report',
            'water_test_report',
        )

class SampleFormSerializer(serializers.ModelSerializer):
    sample = serializers.CharField(allow_blank=True, required=False)
    quantity = serializers.IntegerField(required=False)
    previous_year = serializers.DateField(required=False)
    sample_request = serializers.CharField(required=False, allow_blank=True)
    sample_request_qauntity = serializers.IntegerField(required=False)
    photo_upload = serializers.CharField(required=False, allow_blank=True)
    excepted_result_date = serializers.DateField(required=False)
    sample_given_date = serializers.DateField(required=False)
    excepted_result_photo = serializers.CharField(required=False, allow_blank=True)
    excepted_result_note = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = SampleForm
        fields = [
            'id',
            'farmer',
            'sample',
            'quantity',
            'previous_year',
            'sample_request',
            'sample_request_qauntity',
            'photo_upload',
            'excepted_result_date',
            'sample_given_date',
            'excepted_result_photo',
            'excepted_result_note',
        ]


class CultivationSample(serializers.ModelSerializer):
    farmer_cultivation = CultivationFormReadSerializer(many=True)
    farmer_sample = SampleFormSerializer(many=True)
    class Meta:
        model= FarmerDetails
        fields = ['farmer_cultivation', 'farmer_sample']



class DealerFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealerForm
        fields = [
                'id',
                'branch_name',
                'firm_name',
                'address',
                'safety_deposit_ammount',
                'distributor_bank_account_number',
                'distributor_bank_name',
                'ifsc_or_rtgs',
                'branch_contact_number',
                'tin_number',
                'safety_check_one',
                'safety_check_two',
                'firm_status',
                'dealer_name',
                'dealer_father_name',
                'date_of_birth',
                'dealer_address',
                'dealer_phone_number',
                'heir_guarantor'
        ]

###############--------------Orders--------------############

class OrderPlacingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'



class VendorSerializer(serializers.ModelSerializer):
    vendor_order = OrderPlacingSerializer(many=True)
    class Meta:
        model = Vendors
        fields = [
            'vendor_name',
            'vendor_address',
            'vendor_city',
            'vendor_pin_code',
            'vendor_pan',
            'vendor_gst',
            'vendor_contact',
            'vendor_type',
            'created_on',
            'status',
            'vendor_order'
        ]
##########################Order#######################

class VendorCreate(serializers.ModelSerializer):
    vendor_name = serializers.CharField(required=False, allow_blank=True)
    vendor_address = serializers.CharField(required=False, allow_blank=True)
    vendor_city = serializers.CharField(required=False, allow_blank=True)
    vendor_pin_code = serializers.IntegerField(required=False)
    vendor_pan = serializers.CharField(required=False, allow_blank=True)
    vendor_gst = serializers.CharField(required=False, allow_blank=True)
    vendor_contact = serializers.CharField(required=False, allow_blank=True)
    vendor_type = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False)

    class Meta:
        model = Vendors
        fields = '__all__'

class VendorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = '__all__'


class OrderedItemsSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(required=False, allow_blank=True)
    hsn_sac_code = serializers.CharField(required=False, allow_blank=True)
    item_name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    uom = serializers.CharField(required=False, allow_blank=True)
    qty = serializers.FloatField(required=False)
    discount_amount = serializers.FloatField(required=False)
    rate = serializers.FloatField(required=False)
    total_amount = serializers.FloatField(required=False)
    class Meta:
        model = OrderedItems
        fields = ('id', 'item_code', 'hsn_sac_code', 'item_name', 'description', 'uom', 'qty', 'discount_amount', 'rate', 'total_amount')
        # fields = '__all__'
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }

class PlaceOrderSerializer(serializers.ModelSerializer):
    order_items = OrderedItemsSerializer(many=True)
    po = serializers.CharField(required=False, allow_blank=True)
    shipping_address = serializers.CharField(required=False, allow_blank=True)
    discount_amount = serializers.FloatField(required=False)
    total_amount = serializers.FloatField(required=False)

    class Meta:
        model = Orders
        fields =['id', 'vendor', 'po', 'po_date', 'shipping_address', 'discount_amount', 'total_amount', 'comfirmed', 'created_on', 'order_items']
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }


    def create(self, validated_data):
        ordered_items = validated_data.pop('order_items')
        order1 = Orders.objects.create(**validated_data)
        for ordered_item in ordered_items:
            OrderedItems.objects.create(order=order1, **ordered_item)
        return order1

    def update(self, instance, validated_data):
        # print(validated_data)
        # order_item = validated_data.pop('order_items')
        # print(validated_data.get('shipping_address'))
        instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
        instance.discount_amount = validated_data.get('discount_amount', instance.discount_amount)
        instance.comfirmed = validated_data.get('comfirmed', instance.comfirmed)

        instance.save()

        # order_items = validated_data.get('order_items')
        order_items = validated_data['order_items']
        print(validated_data)

        if order_items:
            for item in order_items:
                # print(item)
                item_id = item.get('id', None)
                
                if item_id:
                    orders_item = OrderedItems.objects.get(id = item_id)
                    orders_item.item_code = item.get('item_code', orders_item.item_code)
                    orders_item.hsn_sac_code = item.get('hsn_sac_code', orders_item.hsn_sac_code)
                    orders_item.item_name = item.get('item_name', orders_item.item_name)
                    orders_item.description = item.get('description', orders_item.description)
                    orders_item.uom = item.get('uom', orders_item.uom)
                    orders_item.qty = item.get('qty', orders_item.qty)
                    orders_item.discount_amount = item.get('discount_amount', orders_item.discount_amount)
                    orders_item.rate = item.get('rate', orders_item.rate)
                    orders_item.save()
                else:
                    OrderedItems.objects.create(order=instance, **item)
                    # print("maddy")
        return instance



class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


    # def update(self, instance, validated_data):
    #     soils = validated_data.pop('soil_type')
    #     crops = validated_data.pop('crop_type')
    #     instance.farmer_name = validated_data.get('farmer_name', instance.farmer_name)
    #     instance.state = validated_data.get('state', instance.state)
    #     instance.district = validated_data.get('district', instance.district)
    #     instance.taluka = validated_data.get('taluka', instance.taluka)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.pin = validated_data.get('pin', instance.pin)
    #     instance.longitude = validated_data.get('longitude', instance.longitude)
    #     instance.latitude = validated_data.get('latitude', instance.latitude)
    #     instance.primary_phone = validated_data.get('primary_phone', instance.primary_phone)
    #     instance.secondary_phone = validated_data.get('secondary_phone', instance.secondary_phone)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.land_area = validated_data.get('land_area', instance.land_area)
    #     instance.soil_color = validated_data.get('soil_color', instance.soil_color)

    #     instance.save()

    #     soils = validated_data.get('soil_type')

    #     crops = validated_data.get('crop_type')

    #     if soils:
    #         for item in soils:
    #             item_id = item.get('id', None)
    #             if item_id:
    #                 soil_type = FarmerSoilType.objects.get(id=item_id)
    #                 soil_type.soil = item.get('soil', soil_type.soil)
    #                 soil_type.save()
    #             else:
    #                 FarmerSoilType.objects.create(farmer=instance, **item)

    #     if crops:
    #         for item in crops:
    #             item_id = item.get('id', None)
    #             if item_id:
    #                 crop_type = FarmerCropType.objects.get(id=item_id)
    #                 crop_type.soil = item.get('soil', crop_type.soil)
    #                 crop_type.save()
    #             else:
    #                 FarmerCropType.objects.create(farmer=instance, **item)
    #     return instance



##########--------------Add New Employee to the organization------------#########
class AddNewEmployeeSerializer(serializers.ModelSerializer):
    phone_no = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    pincode = serializers.IntegerField(required=False)
    father_name = serializers.CharField(required=False, allow_blank=True)
    mother_name = serializers.CharField(required=False, allow_blank=True)
    pan_card = serializers.CharField(required=False, allow_blank=True)
    approved = serializers.BooleanField(required=False, write_only=True)

    class Meta:
        model = Employees
        fields = [
            'user',
            'phone_no',
            'email',
            'address',
            'city',
            'pincode',
            'father_name',
            'mother_name',
            'pan_card',
            'approved'
        ]

class EmployeeListSerializer(serializers.ModelSerializer):
    user_role = RoleSerializer()
    employee_other_details = AddNewEmployeeSerializer()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'user_role', 'employee_other_details']
##########-------------------------HR Payrole-----------##############

class HrUserSerializer(serializers.ModelSerializer):
    user_role = RoleSerializer()
    employee_other_details = AddNewEmployeeSerializer()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'user_role', 'employee_other_details']


##########----------------------Bank Details----------###############

class BankDetailsSerializer(serializers.ModelSerializer):
    phone_no = serializers.CharField(required=False, allow_blank=True)
    bmicr_code = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = BankDetails
        fields = '__all__'



#########----------------------Salary Serializer----------############
class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'



class HrUserDetailSerializer(serializers.ModelSerializer):
    employee_salary = SalarySerializer(many=False)
    employee_bank = BankDetailsSerializer(many=False)
    user_role = RoleSerializer(many=False)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'employee_salary', 'employee_bank', 'user_role']

#########------------Approve Employee serializer--------############
class ApproveEmployeeDetails(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'


class ApproveEmployeesSerializer(serializers.ModelSerializer):
    user_role = RoleSerializer(many=False)
    employee_other_details = ApproveEmployeeDetails()
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'user_role',
            'employee_other_details'
        ]

######---------------Requested Salaries-----------##############
class SalaryRequestedUserSerializer(serializers.ModelSerializer):
    employee_bank = BankDetailsSerializer(many=False)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'employee_bank']

class SalaryRequestedSerializer(serializers.ModelSerializer):
    user = SalaryRequestedUserSerializer(many=False)
    class Meta:
        model=SalaryRequest
        fields = '__all__'

class SalaryRequestPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryRequest
        fields = '__all__'

class UserPayslipSerializer(serializers.ModelSerializer):
    user_role = RoleSerializer()
    employee_other_details = AddNewEmployeeSerializer()
    employee_bank = BankDetails()

    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'email', 'user_role', 'employee_other_details','employee_bank']

class PayslipSerializer(serializers.ModelSerializer):
    user = UserPayslipSerializer()
    basic = serializers.FloatField(required=False)
    hra = serializers.FloatField(required=False)
    conveyance_allowance = serializers.FloatField(required=False)
    deduction = serializers.FloatField(required=False)
    salary_month = serializers.IntegerField(required=False)
    salary_year = serializers.IntegerField(required=False)
    misc_allowance = serializers.FloatField(required=False)
    proffesional_tax = serializers.FloatField(required=False)
    net_salary = serializers.FloatField(required=False)
    net_salary_paybale = serializers.FloatField(required=False)
    created_on = serializers.DateTimeField(format="%Y:%m:%d")
    credited_on = serializers.DateTimeField(format="%Y:%m:%d")

    class Meta:
        model = SalaryRequest
        fields = [
            'user',
            'basic',
            'hra',
            'conveyance_allowance',
            'deduction',
            'salary_month',
            'salary_year',
            'misc_allowance',
            'proffesional_tax',
            'net_salary',
            'net_salary_paybale',
            'created_on',
            'credited_on'
        ]


##################---Appraisals---------##################
class AppraisalsSerializer(serializers.ModelSerializer):
    self_qoute = serializers.CharField(required=False, allow_blank=True)
    manager_qoute = serializers.CharField(required=False, allow_blank=True)
    manager_rating = serializers.FloatField(required=False)
    self_rating = serializers.FloatField(required=False)
    summary = serializers.CharField(required=False, allow_blank=True)
    year = serializers.CharField(required=False)
    status = serializers.BooleanField(required=False)

    class Meta:
        model = Appraisals
        fields = '__all__'