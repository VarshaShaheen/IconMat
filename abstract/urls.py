from django.urls import path
from . import views

urlpatterns = [
    path('submit_abstract/', views.abstract_submission, name='abstract_submission'),
    path('abstract_details/', views.AbstractDetail.as_view(), name='abstract_details'),
    path('view-abstract/', views.view_abstract, name='view_abstract'),
]
