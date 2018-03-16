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
from datetime import date
import time
from datetime import datetime
from time import gmtime, strftime
import random
import string
from django.utils import timezone


class Status(ChoiceEnum):
    Available = "Available"
    Booked = "Booked"
    Maintenance = "Maintenance"
    Occupied = "Occupied"
    CheckedOut = "CheckedOut"

class PaidBy(ChoiceEnum):
    Card = "Card"
    Cash = "Cash"



class RoomTypes(models.Model):
	room_type = models.CharField(max_length=20)
	price = models.FloatField()
	tax = models.FloatField()
	description = models.CharField(max_length=50, null=True)
	updated_on = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.room_type


class Rooms(models.Model):
	room_number = models.CharField(max_length=10, unique=True)
	floor = models.IntegerField()
	status = EnumChoiceField(enum_class=Status, default=Status.Available)
	room_type = models.ForeignKey(RoomTypes, on_delete=models.SET_NULL, null=True, related_name='type_of_room')

	def __str__(self):
		return self.room_number

class Booking(models.Model):
	 room = models.ForeignKey(Rooms, on_delete=models.SET_NULL, related_name='booked_rooms', null=True)
	 customer_first_name = models.CharField(max_length=100)
	 customer_last_name = models.CharField(max_length=100, null=True, blank=True)
	 mobile_number = models.CharField(max_length=13)
	 email = models.EmailField(null=True, blank=True)
	 id_proof_one = models.FileField(null=True, blank=True)
	 id_proof_two = models.FileField(null=True, blank=True)
	 adults = models.IntegerField(default=0)
	 child = models.IntegerField(default=0)
	 check_in = models.DateField(null=True)
	 token_amount = models.FloatField(default=0)
	 check_out = models.DateField(null=True)
	 number_of_days = models.IntegerField(null=True)
	 address = models.CharField(max_length=200, null=True, blank=True)
	 city = models.CharField(max_length=50, blank=True, null=True)
	 taluka = models.CharField(max_length=100, null=True, blank=True)
	 pincode = models.IntegerField(null=True)
	 status = models.BooleanField(default=True)
	 booking_status = EnumChoiceField(enum_class=Status, default=Status.Booked)
	 checked_in = models.BooleanField(default=False)

	 def save(self, *args, **kwargs):
	 	if self.check_in is None:
	 		self.check_in = timezone.localtime(timezone.now())
	 		super(Booking, self).save(*args, **kwargs)
	 	else:
	 		super(Booking, self).save(*args, **kwargs)


	 def __str__(self):
	 	if self.customer_last_name:
	 		return self.customer_first_name+ ' ' + str(self.customer_last_name)
	 	return self.customer_first_name


class RoomStatus(models.Model):
	room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='room')
	from_date = models.DateField(null=True)
	to_date = models.DateField(null=True)
	room_status = EnumChoiceField(enum_class=Status, default=Status.Maintenance)
	booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, related_name='booking', null=True)
	status = models.BooleanField(default=True)



class FoodCategory(models.Model):
	category_name = models.CharField(max_length=20)
	tax = models.FloatField()

	def __str__(self):
		return self.category_name


class AdditionalBill(models.Model):
	booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='additional_bill')
	items = models.CharField(max_length=100, null=True, blank=True)
	qty = models.FloatField(null=True, default=1)
	category = models.CharField(max_length=20, null=True)
	price = models.FloatField(default=0)
	tax = models.FloatField(default=0)
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
	paid_by = EnumChoiceField(enum_class=PaidBy, default=PaidBy.Cash)
	additional_amount = models.FloatField(null=True, default=0)
	room_price = models.FloatField(null=True, default=0)
	tax = models.FloatField(null=True, default=0)
	room_price_total = models.FloatField(null=True, default=0)
	number_of_days = models.FloatField(null=True, default=0)
	total_amount = models.FloatField(null=True, default=0)
	invoice = models.FileField(null=True)

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

	@property
	def room_price_calculate(self):
		number_of_days = self.number_of_days
		tax = self.tax
		token = self.booking.token_amount
		booking = Booking.objects.filter(id=self.booking.id).first()
		room_price = booking.room.room_type.price
		actual_amount = float(number_of_days) * float(room_price)
		one_percent_tax = float(actual_amount)/100
		calculate_tax = float(one_percent_tax) * tax
		final_amount = float(actual_amount)+float(calculate_tax)-float(token)
		return final_amount

	def save(self, *args, **kwargs):
		booking = Booking.objects.filter(id=self.booking.id).first()
		room_of_price = booking.room.room_type.price
		self.total_amount = self.calculate_bill
		self.room_price_total = self.room_price_calculate
		super(Billing, self).save(*args, **kwargs)


	
	def __str__(self):
		return self.total_amount