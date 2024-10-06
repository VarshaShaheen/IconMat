from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL to view the home function
    path('symposia/', views.symposia_list, name='symposia_list'),  # URL to view the synopsis_list function
]
