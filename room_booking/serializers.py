from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.conf import settings
from collections import namedtuple
from enumchoicefield import ChoiceEnum, EnumChoiceField
from django.http import JsonResponse
from django.db.models import Q

import datetime
from datetime import date
import time
from datetime import datetime
from time import gmtime, strftime
from django.utils import timezone
from dateutil.parser import parse

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


class RoomStatusSerializer(serializers.ModelSerializer):
	room_number = serializers.CharField(required=False)
	floor = serializers.IntegerField(required=False)

	class Meta:
		model = Rooms
		fields = '__all__'


class RoomForRoomStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rooms
		fields = ['id','room_number', 'room_type', 'floor']


# (Q(username=email) | Q(email=email))
class BookingSerializerForRoom(serializers.ModelSerializer):
	customer_first_name = serializers.CharField(required=False, allow_blank=True)
	customer_last_name = serializers.CharField(required=False, allow_blank=True)
	check_in = serializers.DateField(required=False)
	check_out = serializers.DateField(required=False)
	status = serializers.BooleanField(required=False, read_only=True)
	checked_in = serializers.BooleanField(required=False, read_only=True)
	booking_status = EnumChoiceField(enum_class=Status)
	
	class Meta:
		model = Booking
		fields = [
			'id',
			'customer_first_name',
			'customer_last_name',
			'check_in',
			'check_out',
			'status',
			'checked_in',
			'booking_status'
		]

class RoomGetSerializer(serializers.ModelSerializer):
	bookings = serializers.SerializerMethodField()
	status = EnumChoiceField(enum_class=Status)
	room_number = serializers.CharField(required=False)
	floor = serializers.IntegerField(required=False)
	room_type = RoomTypeSerializer()

	def get_bookings(self, rooms):
		today = datetime.strftime(datetime.now(), "%Y-%m-%d")
		today=(datetime.strptime(today, '%Y-%m-%d')).date()
		bookings_obj = None
		qs = Booking.objects.filter(room=rooms, check_in__gte=today).filter(check_out__lte=today)
		booking = Booking.objects.filter(room=rooms)
		for boo in booking:
			if boo.check_in<=today and today<=boo.check_out:
				serializer = BookingSerializerForRoom(instance=boo, many=False)
				return serializer.data

	class Meta:
		model = Rooms
		fields = [
			'id',
			'status',
			'room_number',
			'floor',
			'room_type',
			'bookings'
		]


class FoodCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = FoodCategory
		fields = '__all__'


class AdditionalBillSerializer(serializers.ModelSerializer):
	# total = serializers.FloatField(required=False)
	attachment = serializers.FileField(required=False)
	class Meta:
		model = AdditionalBill
		fields = '__all__'



class BookingSerializer(serializers.ModelSerializer):
	customer_first_name = serializers.CharField(required=False, allow_blank=True)
	customer_last_name = serializers.CharField(required=False, allow_blank=True)
	adults = serializers.IntegerField(required=False)
	child = serializers.IntegerField(required=False)
	# booking_id = serializers.CharField(required=False)
	address = serializers.CharField(required=False, allow_blank=True)
	check_in = serializers.DateField(required=False)
	check_out = serializers.DateField(required=False)
	number_of_days = serializers.IntegerField(required=False)
	email = serializers.EmailField(required=False, allow_blank=True)
	id_proof_one = serializers.FileField(required=False)
	id_proof_two = serializers.FileField(required=False)
	token_amount = serializers.FloatField(required=False)
	pincode = serializers.IntegerField(required=False)
	status = serializers.BooleanField(required=False, read_only=True)
	checked_in = serializers.BooleanField(required=False, read_only=True)
	taluka = serializers.CharField(required=False, allow_blank=True)
	booking_status = EnumChoiceField(enum_class=Status)
	
	def create(self, validated_data):
		booking1 = Booking.objects.create(**validated_data)
		RoomStatus.objects.create(booking=booking1, room=booking1.room, from_date=booking1.check_in, to_date=booking1.check_out, room_status=Status.Booked)
		return booking1

	class Meta:
		model = Booking
		fields = '__all__'


class CheckInBookingSerializer(serializers.ModelSerializer):
	customer_first_name = serializers.CharField(required=False, allow_blank=True)
	customer_last_name = serializers.CharField(required=False, allow_blank=True)
	adults = serializers.IntegerField(required=False)
	child = serializers.IntegerField(required=False)
	# booking_id = serializers.CharField(required=False)
	address = serializers.CharField(required=False, allow_blank=True)
	check_in = serializers.DateField(required=False)
	check_out = serializers.DateField(required=False)
	number_of_days = serializers.IntegerField(required=False)
	email = serializers.EmailField(required=False, allow_blank=True)
	id_proof_one = serializers.FileField(required=False)
	id_proof_two = serializers.FileField(required=False)
	token_amount = serializers.FloatField(required=False)
	pincode = serializers.IntegerField(required=False)
	status = serializers.BooleanField(required=False, read_only=True)
	checked_in = serializers.BooleanField(required=False, read_only=True)
	taluka = serializers.CharField(required=False, allow_blank=True)
	booking_status = EnumChoiceField(enum_class=Status)

	def create(self, validated_data):
		check_in_instance = Booking.objects.create(checked_in=True, booking_status = Status.Occupied, **validated_data)
		RoomStatus.objects.create(booking=check_in_instance, room=check_in_instance.room, from_date=check_in_instance.check_in, to_date=check_in_instance.check_out, room_status=Status.Occupied)
		return check_in_instance
	
	class Meta:
		model = Booking
		fields = '__all__'

class BookingGetSerializer(serializers.ModelSerializer):
	additional_bill = AdditionalBillSerializer(many=True)
	room = RoomForRoomStatusSerializer()

	class Meta:
		model = Booking
		fields = [
					'id', 
					'customer_first_name',
					'customer_last_name', 
					'adults',
					'check_in',
					'room',
					'check_out',
					'child',
					'address',
					'email',
					'mobile_number',
					'city',
					'id_proof_one',
					'id_proof_two',
					'taluka',
					'checked_in',
					'booking_status',
					'token_amount',
					'pincode',
					'additional_bill'
					]



class BillingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Billing
		fields = '__all__'


class BookingBillingSerializer(serializers.ModelSerializer):
	additional_bill = AdditionalBillSerializer(many=True)
	booking_bill = BillingSerializer(required=False)

	check_in = serializers.DateTimeField(format="%Y-%m-%d")
	check_out = serializers.DateTimeField(format="%Y-%m-%d")

	class Meta:
		model = Booking
		fields = [
			'id', 
			'customer_first_name',
			'customer_last_name', 
			'adults',
			'room',
			'check_in',
			'check_out',
			'child',
			'address',
			'email',
			'id_proof_one',
			'id_proof_two',
			'taluka',
			'token_amount',
			'pincode',
			'additional_bill',
			'booking_bill'
		]

class BookingInfoSerializerRoom(serializers.ModelSerializer):
	room_type = RoomTypeSerializer()
	class Meta:
		model = Rooms
		fields = ['id', 'room_number', 'floor', 'room_type']


class BookingInfoSerializer(serializers.ModelSerializer):
	additional_bill = AdditionalBillSerializer(many=True)
	room = BookingInfoSerializerRoom()
	booking_bill = BillingSerializer(required=False)
	# check_in = serializers.DateTimeField(format="%Y-%m-%d")

	class Meta:
		model = Booking
		fields = [
			'id', 
			'room',
			'customer_first_name',
			'customer_last_name', 
			'adults',
			'check_in',
			'check_out',
			'child',
			'address',
			'email',
			'id_proof_one',
			'id_proof_two',
			'taluka',
			'checked_in',
			'booking_status',
			'token_amount',
			'pincode',
			'additional_bill',
			'booking_bill'
		]

class RoomStatusBookingSerializer(serializers.ModelSerializer):
	additional_bill = AdditionalBillSerializer(many=True)
	booking_bill = BillingSerializer(required=False)
	# check_in = serializers.DateTimeField(format="%Y-%m-%d")

	class Meta:
		model = Booking
		fields = [
			'id', 
			'room',
			'customer_first_name',
			'customer_last_name', 
			'adults',
			'check_in',
			'check_out',
			'child',
			'address',
			'email',
			'id_proof_one',
			'id_proof_two',
			'taluka',
			'checked_in',
			'booking_status',
			'token_amount',
			'pincode',
			'additional_bill',
			'booking_bill'
		]



class RoomStatusSerializer(serializers.ModelSerializer):
	room = RoomForRoomStatusSerializer(many=False)
	booking = RoomStatusBookingSerializer(many=False)

	class Meta:
		model = RoomStatus
		fields = ['from_date', 'to_date', 'room', 'booking', 'room_status', 'room']