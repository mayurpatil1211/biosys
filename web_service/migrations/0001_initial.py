# Generated by Django 2.0 on 2018-04-03 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('activity_date', models.DateField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_activity', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppliedLeave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_leave', models.CharField(max_length=100)),
                ('leave_from', models.DateField(blank=True, null=True)),
                ('to_leave', models.DateField(blank=True, null=True)),
                ('number_of_days', models.FloatField(max_length=5)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(default=False)),
                ('appliedOn', models.DateField(auto_now_add=True)),
                ('actionOn', models.DateTimeField(blank=True, null=True)),
                ('declined', models.BooleanField(default=False)),
                ('appliedBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_leave', to=settings.AUTH_USER_MODEL)),
                ('approvedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appraisals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self_qoute', models.CharField(blank=True, max_length=200, null=True)),
                ('manager_qoute', models.CharField(blank=True, max_length=200, null=True)),
                ('manager_rating', models.FloatField(default=0, null=True)),
                ('self_rating', models.FloatField(default=0, null=True)),
                ('summary', models.CharField(default=0, max_length=200, null=True)),
                ('year', models.CharField(max_length=10, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete='CASCADE', related_name='appraisals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clock_in', models.DateTimeField(null=True)),
                ('clock_out', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_attendance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=200)),
                ('bank_name', models.CharField(max_length=100)),
                ('ifsc_code', models.CharField(max_length=50)),
                ('account_type', models.CharField(max_length=20)),
                ('bank_address', models.CharField(max_length=200)),
                ('phone_no', models.CharField(blank=True, max_length=13, null=True)),
                ('bmicr_code', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_bank', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CultivationForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_year', models.DateField(blank=True, null=True)),
                ('crop_details', models.CharField(blank=True, max_length=200, null=True)),
                ('crop_type', models.CharField(blank=True, max_length=50, null=True)),
                ('pesticides', models.CharField(blank=True, max_length=100, null=True)),
                ('deases', models.CharField(blank=True, max_length=100, null=True)),
                ('chemicals', models.CharField(blank=True, max_length=100, null=True)),
                ('fertilizer', models.CharField(blank=True, max_length=200, null=True)),
                ('soil_test_report', models.CharField(blank=True, max_length=1000, null=True)),
                ('water_test_report', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DealerForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(blank=True, max_length=200, null=True)),
                ('firm_name', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('safety_deposit_ammount', models.FloatField(blank=True, null=True)),
                ('distributor_bank_account_number', models.CharField(blank=True, max_length=30, null=True)),
                ('distributor_bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ifsc_or_rtgs', models.CharField(blank=True, max_length=100, null=True)),
                ('branch_contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('tin_number', models.CharField(blank=True, max_length=100, null=True)),
                ('safety_check_one', models.CharField(blank=True, max_length=100, null=True)),
                ('safety_check_two', models.CharField(blank=True, max_length=100, null=True)),
                ('firm_status', models.CharField(blank=True, max_length=20, null=True)),
                ('dealer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('dealer_father_name', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('dealer_address', models.CharField(blank=True, max_length=500, null=True)),
                ('dealer_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('heir_guarantor', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ducument_file', models.FileField(upload_to='documents/')),
                ('document_description', models.CharField(blank=True, max_length=200, null=True)),
                ('file_type', models.CharField(blank=True, max_length=20, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_document', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appliedOn', models.DateField(auto_now_add=True)),
                ('count', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(blank=True, max_length=13, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('father_name', models.CharField(blank=True, max_length=50, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=50, null=True)),
                ('pan_card', models.CharField(blank=True, max_length=100, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('approved_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_other_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('expense_type', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('declined', models.BooleanField(default=False)),
                ('approvedOn', models.DateField(auto_now_add=True)),
                ('actionOn', models.DateField(auto_now_add=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity', to='web_service.Activity')),
                ('aproved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aproved_expense', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_expense', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmerCropType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FarmerDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farmer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('taluka', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('pin', models.CharField(blank=True, max_length=10, null=True)),
                ('longitude', models.CharField(blank=True, max_length=50, null=True)),
                ('latitude', models.CharField(blank=True, max_length=50, null=True)),
                ('primary_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('secondary_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('land_area', models.CharField(blank=True, max_length=500, null=True)),
                ('soil_color', models.CharField(blank=True, max_length=200, null=True)),
                ('form_filled_on', models.DateField(auto_now_add=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('activity', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_farmer', to='web_service.Activity')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmerSoilType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soil', models.CharField(blank=True, max_length=100, null=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soil_type', to='web_service.FarmerDetails')),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('reason', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(blank=True, max_length=100, null=True)),
                ('item_code', models.CharField(blank=True, max_length=100, null=True)),
                ('hsn_sac_code', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('uom', models.CharField(blank=True, max_length=200, null=True)),
                ('rate', models.FloatField(blank=True, null=True)),
                ('discount_amount', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Leaves',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_sick_leave', models.FloatField()),
                ('total_sick_leave', models.FloatField()),
                ('balance_casual_leave', models.FloatField()),
                ('total_casual_leave', models.FloatField()),
                ('balance_earned_leave', models.FloatField()),
                ('total_earned_leave', models.FloatField()),
                ('balance_compoff_leave', models.FloatField()),
                ('total_compoff_leave', models.FloatField()),
                ('total_lop', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_assigned_leaves', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(blank=True, max_length=200, null=True)),
                ('hsn_sac_code', models.CharField(blank=True, max_length=200, null=True)),
                ('item_name', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('uom', models.CharField(blank=True, max_length=200, null=True)),
                ('qty', models.FloatField(blank=True, null=True)),
                ('discount_amount', models.FloatField(blank=True, null=True)),
                ('rate', models.FloatField(blank=True, null=True)),
                ('total_amount', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_address', models.CharField(blank=True, max_length=1000, null=True)),
                ('discount_amount', models.FloatField(blank=True, null=True)),
                ('total_amount', models.FloatField(blank=True, null=True)),
                ('comfirmed', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('po_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_type', models.CharField(max_length=20)),
                ('department', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_role', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoleTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic', models.FloatField()),
                ('hra', models.FloatField()),
                ('conveyance_allowance', models.FloatField(null=True)),
                ('misc_allowance', models.FloatField(null=True)),
                ('proffesional_tax', models.FloatField(null=True)),
                ('net_salary', models.FloatField(null=True)),
                ('net_salary_anum', models.FloatField(null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_salary', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalaryRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic', models.FloatField(null=True)),
                ('hra', models.FloatField(null=True)),
                ('conveyance_allowance', models.FloatField(null=True)),
                ('deduction', models.FloatField(null=True)),
                ('salary_month', models.IntegerField()),
                ('salary_year', models.IntegerField()),
                ('misc_allowance', models.FloatField(null=True)),
                ('proffesional_tax', models.FloatField(null=True)),
                ('net_salary', models.FloatField(null=True)),
                ('net_salary_paybale', models.FloatField(null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('credited', models.BooleanField(default=False)),
                ('credited_on', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salaries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SampleForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('previous_year', models.DateField(blank=True, null=True)),
                ('sample_request', models.CharField(blank=True, max_length=200, null=True)),
                ('sample_request_qauntity', models.IntegerField(blank=True, null=True)),
                ('sample_given_date', models.DateField(auto_now_add=True, null=True)),
                ('photo_upload', models.CharField(blank=True, max_length=1000, null=True)),
                ('excepted_result_date', models.DateField(blank=True, null=True)),
                ('excepted_result_photo', models.CharField(blank=True, max_length=1000, null=True)),
                ('excepted_result_note', models.CharField(blank=True, max_length=500, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farmer_sample', to='web_service.FarmerDetails')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(blank=True, max_length=200, null=True)),
                ('vendor_address', models.CharField(blank=True, max_length=500, null=True)),
                ('vendor_city', models.CharField(blank=True, max_length=50, null=True)),
                ('vendor_pin_code', models.IntegerField(blank=True, null=True)),
                ('vendor_pan', models.CharField(blank=True, max_length=50, null=True)),
                ('vendor_gst', models.CharField(blank=True, max_length=100, null=True)),
                ('vendor_contact', models.IntegerField(blank=True, null=True)),
                ('vendor_type', models.CharField(blank=True, max_length=100, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='VendorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_shipping_address', to='web_service.Vendors'),
        ),
        migrations.AddField(
            model_name='orders',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_order', to='web_service.Vendors'),
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='web_service.Orders'),
        ),
        migrations.AddField(
            model_name='farmercroptype',
            name='farmer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crop_type', to='web_service.FarmerDetails'),
        ),
        migrations.AddField(
            model_name='cultivationform',
            name='farmer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farmer_cultivation', to='web_service.FarmerDetails'),
        ),
    ]
