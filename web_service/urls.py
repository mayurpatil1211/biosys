from django.conf.urls import url
from . import views


urlpatterns=[
	url(r'^register/', views.register, name='register'),
	url(r'userLogin', views.login, name='userlogin'),
	url(r'^logout/$', views.logout, name='logout'),
	
	url(r'^attendance/', views.AttendanceCreate.as_view()),

	url(r'^forgot_password$', views.forgot_password, name='forgot_password'),

	url(r'^add_employee', views.AddEmployeeView.as_view(), name='add_employee'),

	url(r'^approve_employee', views.ApproveEmployee.as_view(), name='approve_employee'),

	###########Salary################
	url(r'^salary_credited$', views.salary_credited, name='salary_credited'),
	url(r'^salary_request$', views.salary_request, name='salary_request'),
	url(r'^salary_requested$', views.SalaryRequested.as_view(), name='salary_requested'),
	url(r'^salary/(?P<user>[0-9]+)$', views.SalaryIndividual.as_view(), name='individual_salary'),
	url(r'^salary_paid/(?P<user_id>[0-9]+)$', views.SalaryRequestedIndividual.as_view(), name='salary_requested_history'),
	url(r'^salary', views.SalaryView.as_view(), name='salary'),



	###########Bank Details###########
	url(r'^bank_details/(?P<user>[0-9]+)', views.BankDetailsIndividual.as_view(), name='individual_bank_details'),
	url(r'^bank_details', views.BankDetailsView.as_view(), name='bank_details'),


	###########HR API for user details#######
	url(r'^hr/user_list/all$', views.HrUserListView.as_view(), name='user_list_hr'),
	url(r'^hr/user_details/(?P<user>[0-9]+)', views.HrUsersDetailsView.as_view(), name='user_details_hr'),


	url(r'^activity/(?P<activity_id>[0-9]+)/$', views.DeleteActivity.as_view(), name='delete_activity'),
	url(r'^activity/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',views.ActivityGetList.as_view()),
	url(r'^activity/', views.ActivityAddList.as_view()),

	url(r'^expense/manager$', views.ManagerExpenseView.as_view()),
	url(r'^expense/(?P<user_id>[0-9]+)$', views.ExpenseIndividual.as_view(), name='individual_expense'),
	url(r'^expense_approve$', views.approve_expense, name='approve_expense'),
	url(r'^expense/', views.ExpenseAddList.as_view()),

	##############Employee Document################
	url(r'^employee/document$', views.EmployeeDocumentView.as_view(), name='employee_document'),
	url(r'^employee/document/(?P<user>[0-9]+)$', views.EmployeeDocumentIndividual.as_view(), name='employee_document_individual'),



	url(r'^holidays$', views.HolidayView.as_view(), name='holidays'),
	url(r'^leave/apply$', views.apply_leave, name='apply_leave'),
	url(r'^leaves$', views.MainLeaveView.as_view(), name='leave_assign'),
	url(r'^leaves/applied$', views.AppliedLeaveViewAPI.as_view(), name='applied_leaves'),
	url(r'^leave/approve$', views.approve_leave, name='leave_approve'),
	url(r'^leave/history/(?P<user_id>[0-9]+)', views.AppliedLeaveUserHistory.as_view(), name="leave_histody"),
	url(r'^leave/balance/(?P<user_id>[0-9]+)$', views.EmployeeBalanceLeave.as_view(), name='balance_leave'),
	url(r'^leave/info/(?P<user_id>[0-9]+)/(?P<month>[0-9]+)/(?P<year>[0-9]+)$', views.LeaveUserInfo.as_view(), name='leave_info'),
	url(r'^leave/manager$', views.ManagerLeaveView.as_view(), name='leave_info_manager'),

	url(r'^farmer_details/add$', views.add_farmer_details, name='add_farmer_details'),
	url(r'^farmer_details$', views.FarmerDetailsClass.as_view(), name='list_farmer_details'),
	url(r'^farmer_details/update$', views.upadte_farmer_details_form, name='upadte_farmer_details_form'),
	url(r'^farmer_individual/(?P<activity_id>[0-9]+)/(?P<user_id>[0-9]+)$', views.FarmerDetailsIndividual.as_view(), name='user_activity_farmer_detail'),
	url(r'^farmer_individual/(?P<user_id>[0-9]+)$', views.FarmerDetailsUser.as_view(), name='user_farmer_detail'),

	url(r'^farmer_list/(?P<user_id>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)$', views.FarmerListViewBasedOnUserDate.as_view(), name='user_date_farmer_form'),
	url(r'^farmer_list/(?P<user_id>[0-9]+)$', views.FarmerListViewBasedOnUser.as_view(), name='user_farmer_form'),

	# url(r'^cultivationForm/(?P<activity_id>[0-9]+)$', views.CultivationFarmerFormView.as_view(), name='cultivationFarmerForm'),
	url(r'^cultivationForm$', views.CultivationFormView.as_view(), name='cultivationForm'),
	url(r'^cultivationForm/individual/(?P<farmer_id>[0-9]+)$', views.CultivationGetView.as_view(), name='individual_cultivation'),

	url(r'^sampleForm$', views.SampleFormView.as_view(), name='sampleForm'),
	url(r'^sampleForm/farmer/(?P<farmer_id>[0-9]+)$', views.SampleFarmerFormView.as_view(), name='sampleActivityForm'),
	url(r'^sampleForm/(?P<id>[0-9]+)$', views.SampleIndividualForm.as_view(), name='sampleIndividualForm'),

	url(r'^cultivation_sampleFroms/(?P<farmer_id>[0-9]+)$', views.CultivationSampleFormView.as_view(), name='cultivationAndSampleForm'),

	url(r'^dealer$', views.DealerFormView.as_view(), name='dealer_details'),
	url(r'^dealer/(?P<id>[0-9]+)$', views.DealerIndividual.as_view(), name='dealer_single_details'),

	# url(r'^place_order$', views.VendorDetails.as_view(), name='place_orders'),
	url(r'^vendor/(?P<id>[0-9]+)$', views.VendorsIndividiual.as_view(), name='vendor'),
	url(r'^orders$', views.OrderPlacingView.as_view(), name='orders'),

	url(r'^vendors$', views.VendorCreateView.as_view(), name='vendor_details'),
	url(r'^vendors/shipping_address/(?P<vendor_id>[0-9]+)$', views.ShippingAddressVendors.as_view(), name='individual_vendor_shipping'),
	url(r'^vendors/shipping_address', views.ShippingAddressView.as_view(), name='vendors_shipping_address'),
	url(r'^place_order$', views.PlacingOrders.as_view(), name='place_orders'),

]