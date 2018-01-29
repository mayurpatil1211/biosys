from django.shortcuts import render
from .models import *
from .serializers import *

from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.utils import timezone

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

class RoomTypeView(APIView):
	def post(self, request, format=None):
		if request.data:
			serializers = RoomTypeSerializer(data=request.data)
			if serializers.is_valid():
				serializers.save()
				return	JsonResponse({'message':'Room type saved Successfully'}, status=201)
			return JsonResponse({'message': 'Bad String'}, status=400)
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

			roomType = RoomTypes.objects.get(id = id)
			serializers = RoomTypeSerializer(roomType, data=request.data)
			if serializers.is_valid():
				serializers.save()
				return JsonResponse({'message':'Room type updated Successfully'}, status=200)
			return JsonResponse({'message':'Bad String'}, status=400)
		return JsonResponse({'message':'Bad Request'}, status=400)

	def delete(self, request, format=None):
		if request.data:
			try:
				id = request.data['id']
			except(KeyError)as e:
				id= None

			roomType = RoomTypes.objects.get(id = id)
			if roomType:
				roomType.delete()
				return JsonResponse({'message':'Room type deleted Successfully'}, status=200)
			return JsonResponse({'message':'Room type Not Found'}, status=400)
		return JsonResponse({'message':'Bad Request'}, status=400)



class FoodCategoryView(APIView):
	def post(self, request, format=None):
		if request.data:
			serializers = FoodCategorySerializer(data=request.data)
			if serializers.is_valid():
				serializers.save()
				return JsonResponse({'message':'Food Category Added Successfully'}, status=201)
			return JsonResponse({'message':'Bad String'}, status=400)
		return JsonResponse({'message':'Bad Request'}, status=400)

	def get(self, request, format=None):
		food_categories = FoodCategory.objects.all()
		serializers = FoodCategorySerializer(food_categories, many=True)
		return Response(serializers.data)

	def put(self, request, format=None):
		if request.data:
			food_category = FoodCategory.objects.get(id=request.data['id'])
			if food_category:
				serializers = FoodCategorySerializer(food_category, data=request.data)
				if serializers.is_valid():
					serializers.save()
					return JsonResponse({'message':'Food Category updated Successfully'}, status=200)
				return JsonResponse({'message':'Bad String'}, status=400)
			return JsonResponse({'message':'Not Found'}, status=400)
		return JsonResponse({'message':'Bad Request'}, status=400)

	def delete(self, request, format=None):
		if request.data:
			food_category = FoodCategory.objects.get(id=request.data['id'])
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
			return JsonResponse({"message":"Bad String"}, status=400)
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
			room = Rooms.objects.get(id = id)
			if room:
			 	serializers = RoomSerializer(room, data=request.data)
			 	if serializers.is_valid():
			 		serializers.save()
			 		return JsonResponse({'message':'Room details updated Successfully'}, status=200)
			 	return JsonResponse({'message':'Bad String'}, status=400)
			return JsonResponse({'message':'Room not Found'}, status=400)
		return JsonResponse({'message':'Bad Request'}, status=400)


class BookingView(APIView):
	def post(self, request, format=None):
		if request.data:
			try:
				room_id = request.data['room']
			except(KeyError)as e:
				room_id = None
			room = Rooms.objects.get(id=room_id)
			if room:
				if room.status == Status.Available:
					serializers = BookingSerializer(data=request.data)
					if serializers.is_valid():
						serializers.save()
						room.status = Status.Unavailable
						room.save()
						return JsonResponse({'message':'Room Booked Successfully'}, status=200)
					return JsonResponse({'message':'Bad String'}, status=400)
				return JsonResponse({'message':'Sorry, Room is '+ str(room.status) +' at this moment'}, status=400)
			return JsonResponse({'message':'Sorry, Room Not Found'}, status=400)
		return JsonResponse({'message':'Bad Request'}, status=400)

	def get(self, request, format=None):
		bookings = Booking.objects.filter(status=True)
		serializers = BookingSerializer(bookings, many=True)
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
				return JsonResponse({'message':'Bad String'}, status=400)
			return JsonResponse({'message':'Invalid, Booking Not Found'}, status=400)
		return JsonResponse({'message':'Bad Request'}, status=400)


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
				return JsonResponse({'message':'Bad String'}, status=400)
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
				additional = AdditionalBill.objects.get(id=id)
				if additional:
					serializers = AdditionalBillSerializer(additional, data=request.data)
					if serializers.is_valid():
						serializers.save()
						return JsonResponse({'message':'Customer Bill Updated'}, status=200)
					return JsonResponse({'message':'Bad String'}, status=400)
				return JsonResponse({'message':'Not Found'}, status=400)
			return JsonResponse({'message': 'ID is reqired'}, status=400)
		return JsonResponse({'message':'Bad Request'}, status=400)

	def delete(self, request, format=None):
		if request.data:
			try:
				id = request.data['id']
			except(KeyError)as e:
				id = None

			try:
				additional = AdditionalBill.objects.get(id = id)
			except(Exception)as e:
				return JsonResponse({'message':'Requested Bill Does Not Exist'}, status=400)

			if additional:
				additional.delete()
				return JsonResponse({'message':'Requested Bill Deleted Successfully'}, status=200)
			return JsonResponse({'message':'Not Found'}, status=400)
		return JsonResponse({'message':'Bad Request'}, status=400)

	def get(self, request, format=None):
		additional = AdditionalBill.objects.all()
		serializers = AdditionalBillSerializer(additional, many=True)
		return Response(serializers.data)

#-----CheckOut------
@api_view(['POST'])
def check_out(request):
	if request.data:
		try:
			booking_id = request.data['booking']
		except(KeyError)as e:
			return JsonResponse({'message':'Please Tell Us which booking'}, status=400)

		booking = Booking.objects.get(id=booking_id)
		if booking:
			booking.check_out = timezone.localtime(timezone.now())
			booking.status=False
			booking.room.status = Status.Available
			print(booking.room.status)
			booking.room.save()
			start_date = (booking.check_in).strftime("%Y-%m-%d")
			end_date = (booking.check_out).strftime("%Y-%m-%d")
			start_date1 = datetime.strptime(str(start_date), "%Y-%m-%d")
			end_date1 = datetime.strptime(str(end_date), "%Y-%m-%d")
			diff = abs((end_date1-start_date1).days)
			booking.number_of_days = diff+1
			booking.save()
			final_bill = bill_on_checkout(booking.id)
			serializers = BookingBillingSerializer(booking)
			
			return Response(serializers.data)
			# return JsonResponse({'message':'Checked Out'}, status=200)
		return JsonResponse({'message':'Booking Not Found'}, status=400)
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
		print('bill added')
		return 1
	return 0

def calculate_additional_bill(booking_id):
	add_bill = AdditionalBill.objects.filter(booking=booking_id).all()
	total = 0
	for bill in add_bill:
		total += bill.total
	print(total)
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
