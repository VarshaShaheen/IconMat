from django.urls import path
from . import views

urlpatterns = [
	path('initiate/', views.initiate_payment, name='initiate_payment'),
	path('process/', views.process_payment, name='process_payment'),
	path('status/', views.handle_payment_status, name='payment_status'),

]
