import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from enumchoicefield import ChoiceEnum, EnumChoiceField
import uuid
import datetime
import random
import string

class RoomTypes(models.Model):
	room_type = models.CharField(max_length=20)
	price = models.FloatField()
	tax = models.FloatField()
	description = models.CharField(max_length=50, null=True)
	updated_on = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.room_type

class Status(ChoiceEnum):
    Unavailable = "Unavailable"
    Available = "Available"
    Booked = "Booked"



class Rooms(models.Model):
	room_number = models.CharField(max_length=10, unique=True)
	floor = models.IntegerField()
	status = EnumChoiceField(enum_class=Status, default=Status.Available)
	room_type = models.ForeignKey(RoomTypes, on_delete=models.SET_NULL, null=True, related_name='type_of_room')

	def __str__(self):
		return self.room_number



class Booking(models.Model):
	 room = models.ForeignKey(Rooms, on_delete=models.SET_NULL, related_name='booked_rooms', null=True)
	 customer_name = models.CharField(max_length=100)
	 mobile_number = models.CharField(max_length=13)
	 email = models.EmailField(null=True, blank=True)
	 id_proof = models.FileField(null=True, blank=True)
	 adults = models.IntegerField(null=True)
	 child = models.IntegerField(null=True)
	 check_in = models.DateTimeField(auto_now_add=True)
	 token_amount = models.FloatField(null=True, blank=True)
	 check_out = models.DateTimeField(null=True)
	 number_of_days = models.IntegerField(null=True)
	 address = models.CharField(max_length=200, null=True, blank=True)
	 city = models.CharField(max_length=50, blank=True, null=True)
	 pincode = models.IntegerField(null=True)
	 status = models.BooleanField(default=True)

	 def __str__(self):
	 	return self.customer_name

class FoodCategory(models.Model):
	category_name = models.CharField(max_length=20)
	tax = models.FloatField()

	def __str__(self):
		return self.category_name


class AdditionalBill(models.Model):
	booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='additional_bill')
	items = models.CharField(max_length=100, null=True, blank=True)
	qty = models.FloatField(null=True)
	category = models.CharField(max_length=20, null=True)
	price = models.FloatField(null=True)
	tax = models.FloatField(null=True)
	total = models.FloatField(null=True)
	attachment = models.FileField(null=True)

	@property
	def calculate_bill(self):
		qty = self.qty
		price = self.price
		tax = self.tax

		actual_amount = float(qty) * float(price)
		one_percent_tax = float(actual_amount)/100
		calculate_tax = float(one_percent_tax) * tax
		final_amount = float(actual_amount)+float(calculate_tax)
		return final_amount

	def save(self, *args, **kwargs):
		self.total = self.calculate_bill
		super(AdditionalBill, self).save(*args, **kwargs)

	def __str__(self):
		return self.items

class Billing(models.Model):
	booking = models.OneToOneField(Booking, on_delete=models.SET_NULL, related_name='booking_bill', null=True)
	additional_amount = models.FloatField(null=True)
	room_price = models.FloatField(null=True)
	tax = models.FloatField(null=True)
	number_of_days = models.FloatField(null=True)
	total_amount = models.FloatField(null=True)

	@property
	def calculate_bill(self):
		number_of_days = self.number_of_days
		additional_amount = self.additional_amount
		tax = self.tax
		token = self.booking.token_amount

		booking = Booking.objects.filter(id=self.booking.id).first()
		room_price = booking.room.room_type.price

		actual_amount = float(number_of_days) * float(room_price)
		one_percent_tax = float(actual_amount)/100
		calculate_tax = float(one_percent_tax) * tax
		final_amount = float(actual_amount)+float(calculate_tax)+float(additional_amount)-float(token)
		return final_amount

	def save(self, *args, **kwargs):
		booking = Booking.objects.filter(id=self.booking.id).first()
		room_of_price = booking.room.room_type.price
		self.total_amount = self.calculate_bill
		super(Billing, self).save(*args, **kwargs)


	
	def __str__(self):
		return self.total_amount