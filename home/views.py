from django.shortcuts import render
from .models import People

def home(request):
    context = {'people': People.objects.all()}
    return render(request, 'home.html',context)
