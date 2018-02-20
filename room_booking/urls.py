from django.conf.urls import url
from . import views


urlpatterns=[
	url(r'^room_types', views.RoomTypeView.as_view(), name='room_types'),
	url(r'^rooms', views.RoomView.as_view(), name='rooms'),

	url(r'^status', views.RoomStatusIndividualView.as_view(), name='room_status'),
	url(r'^multiple/status', views.RoomStatusMultipleView.as_view(), name='multiple_room_status'),

	url(r'^maintenence/(?P<id>[0-9]+)$', views.RoomMaintenanceView.as_view(), name='room_maintenence'),

	url(r'^food_category', views.FoodCategoryView.as_view(), name='food_category'),
	url(r'^booking_info/(?P<booking_id>[0-9]+)', views.BookingInfo.as_view(), name='booking_info'),
	url(r'^booking', views.BookingView.as_view(), name='booking'),
	url(r'^additional_bill', views.AdditionalBillView.as_view(), name='additional_bill'),
	url(r'^checkout', views.check_out, name='check_out'),
	url(r'^history/booking$', views.BookingHistory.as_view(), name='booking_history'),
	url(r'^history/booking/filter', views.BookingHistoryFilter.as_view(), name	='filter_booking_history'),
	
]
