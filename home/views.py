from django.shortcuts import render
from .models import *


def home(request):
	context = {'chairs'         : People.objects.filter(designation='Conference Chair').order_by('priority'),
	           'patrons'        : People.objects.filter(designation='Conference Patron').order_by('priority'),
	           'symposia'       : Symposia.objects.all(),
	           'carousel_images': Carousel.objects.all()}
	return render(request, 'home.html', context)


def symposia_list(request):
	symposia = Symposia.objects.all()
	return render(request, 'symposia.html', {'symposia': symposia})
