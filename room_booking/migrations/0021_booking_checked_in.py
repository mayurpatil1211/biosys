# Generated by Django 2.0 on 2018-02-21 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking', '0020_auto_20180220_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='checked_in',
            field=models.BooleanField(default=False),
        ),
    ]