from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL to view the home function
    path('symposia/', views.symposia_list, name='symposia_list'),
    path('speakers/', views.speakers, name='speakers'),
    path('programs/', views.programs, name='programs'),
    path('registration/', views.registration, name='registration'),
    path('contact/', views.contact, name='contact'),
    path('tourist_attractions/', views.tourist_attractions, name='tourist_attractions'),
]
