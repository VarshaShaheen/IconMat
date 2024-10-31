from django.urls import path
from . import views

urlpatterns = [
    path('submit_abstract/', views.abstract_submission, name='abstract_submission'),
]
