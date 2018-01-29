from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.conf import settings
from collections import namedtuple
from enumchoicefield import ChoiceEnum, EnumChoiceField
from django.http import JsonResponse

class RoomTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = RoomTypes
		fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
	# room_type = RoomTypeSerializer()
	status = EnumChoiceField(enum_class=Status)

	class Meta:
		model = Rooms
		fields = '__all__'


class RoomGetSerializer(serializers.ModelSerializer):
	room_type = RoomTypeSerializer(many=False)
	status = EnumChoiceField(enum_class=Status)
	class Meta:
		model = Rooms
		fields = '__all__'


class FoodCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = FoodCategory
		fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
	customer_name = serializers.CharField(required=False, allow_blank=True)
	adults = serializers.IntegerField(required=False)
	child = serializers.IntegerField(required=False)
	# booking_id = serializers.CharField(required=False)
	address = serializers.CharField(required=False, allow_blank=True)
	check_out = serializers.DateTimeField(required=False)
	number_of_days = serializers.IntegerField(required=False)
	email = serializers.EmailField(required=False, allow_blank=True)
	id_proof = serializers.FileField(required=False)
	token_amount = serializers.FloatField(required=False)
	pincode = serializers.IntegerField(required=False)
	status = serializers.BooleanField(required=False, read_only=True)

	
	class Meta:
		model = Booking
		fields = '__all__'


class AdditionalBillSerializer(serializers.ModelSerializer):
	# total = serializers.FloatField(required=False)
	attachment = serializers.FileField(required=False)
	class Meta:
		model = AdditionalBill
		fields = '__all__'

class BillingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Billing
		fields = '__all__'


class BookingBillingSerializer(serializers.ModelSerializer):
	additional_bill = AdditionalBillSerializer(many=True)
	booking_bill = BillingSerializer(required=False)

	check_in = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	check_out = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

	class Meta:
		model = Booking
		fields = [
			'room',
			'customer_name',
			'adults',
			'child',
			'check_in',
			'check_out',
			'number_of_days',
			'address',
			'additional_bill',
			'booking_bill',
			'mobile_number',
			'email',
			'id_proof',
			'token_amount',
			'city',
			'pincode'
		]

class BookingInfoSerializer(serializers.ModelSerializer):
	additional_bill = AdditionalBillSerializer(many=True)
	room = RoomGetSerializer()
	check_in = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

	class Meta:
		model = Booking
		fields = [
			'id',
			'room',
			'customer_name',
			'adults',
			'child',
			'check_in',
			'address',
			'additional_bill',
			'mobile_number',
			'email',
			'id_proof',
			'token_amount',
			'city',
			'pincode'
		]