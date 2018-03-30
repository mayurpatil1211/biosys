# Generated by Django 2.0 on 2018-03-30 14:49

from django.db import migrations, models
import django.db.models.deletion
import enumchoicefield.fields
import room_booking.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.CharField(blank=True, max_length=100, null=True)),
                ('qty', models.FloatField(default=1, null=True)),
                ('category', models.CharField(max_length=20, null=True)),
                ('price', models.FloatField(default=0)),
                ('tax', models.FloatField(default=0)),
                ('total', models.FloatField(null=True)),
                ('attachment', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_by', enumchoicefield.fields.EnumChoiceField(default=room_booking.models.PaidBy(2), enum_class=room_booking.models.PaidBy, max_length=4)),
                ('additional_amount', models.FloatField(default=0, null=True)),
                ('room_price', models.FloatField(default=0, null=True)),
                ('tax', models.FloatField(default=0, null=True)),
                ('room_price_total', models.FloatField(default=0, null=True)),
                ('number_of_days', models.FloatField(default=0, null=True)),
                ('total_amount', models.FloatField(default=0, null=True)),
                ('invoice', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_first_name', models.CharField(max_length=100)),
                ('customer_last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_number', models.CharField(max_length=13)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('id_proof_one', models.FileField(blank=True, null=True, upload_to='')),
                ('id_proof_two', models.FileField(blank=True, null=True, upload_to='')),
                ('adults', models.IntegerField(default=0)),
                ('child', models.IntegerField(default=0)),
                ('check_in', models.DateField(null=True)),
                ('token_amount', models.FloatField(default=0)),
                ('check_out', models.DateField(null=True)),
                ('number_of_days', models.IntegerField(null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('taluka', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.IntegerField(null=True)),
                ('status', models.BooleanField(default=True)),
                ('booking_status', enumchoicefield.fields.EnumChoiceField(default=room_booking.models.Status(2), enum_class=room_booking.models.Status, max_length=11)),
                ('checked_in', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20)),
                ('tax', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=10, unique=True)),
                ('floor', models.IntegerField()),
                ('status', enumchoicefield.fields.EnumChoiceField(default=room_booking.models.Status(1), enum_class=room_booking.models.Status, max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='RoomStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('room_status', enumchoicefield.fields.EnumChoiceField(default=room_booking.models.Status(3), enum_class=room_booking.models.Status, max_length=11)),
                ('status', models.BooleanField(default=True)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking', to='room_booking.Booking')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='room_booking.Rooms')),
            ],
        ),
        migrations.CreateModel(
            name='RoomTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('tax', models.FloatField()),
                ('description', models.CharField(max_length=50, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='rooms',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_of_room', to='room_booking.RoomTypes'),
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booked_rooms', to='room_booking.Rooms'),
        ),
        migrations.AddField(
            model_name='billing',
            name='booking',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking_bill', to='room_booking.Booking'),
        ),
        migrations.AddField(
            model_name='additionalbill',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_bill', to='room_booking.Booking'),
        ),
    ]
