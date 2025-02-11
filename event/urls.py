from django.urls import path
from . import views

urlpatterns = [
    path('check-in/', views.scan_qr, name='check_in'),
    path('check-in/qr', views.process_qrcode, name='process_qrcode'),
    path('check-in/id', views.process_iconmat, name='process_iconmat'),

]

