from django.urls import path
from . import views

urlpatterns = [
	path('basic-info/', views.basic_info, name='basic_info'),
	path('conference-info/', views.conference_info, name='conference_info'),
	path('additional-info/', views.additional_info, name='additional_info'),
	path('review-and-payment/', views.review_and_payment, name='review_and_payment'),
	path('completed/', views.registration_completed, name='registration_completed'),
	path('completed/<str:pay_ref_no>/', views.registration_completed, name='registration_completed_ref_no'),
	path('failed/<str:pay_ref_no>/', views.registration_failed, name='registration_failed'),

]
