from django.urls import path
from . import views

urlpatterns = [
    path('check-in/', views.scan_qr, name='check_in'),
    path('check-in/qr', views.process_qrcode, name='process_qrcode'),
    path('check-in/id', views.process_iconmat, name='process_iconmat'),

    path('scan-lunch/', views.scan_lunch, name='scan_lunch'),
    path('scan-dinner/', views.scan_dinner, name='scan_dinner'),
    path('lunch/qr-check-in/', views.lunch_qr_check_in, name='lunch_qr_check_in'),
    path('dinner/qr-check-in/', views.dinner_qr_check_in, name='dinner_qr_check_in'),

]

