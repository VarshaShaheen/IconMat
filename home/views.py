from django.shortcuts import render
from .models import *


def home(request):
	context = {'chairs'         : People.objects.filter(designation='Conference Chair').order_by('priority'),
	           'patrons'        : People.objects.filter(designation='Conference Patron').order_by('priority'),
	           'speakers'       : Speaker.objects.all().order_by('priority'),
	           'advisory_committee': AdvisoryCommittee.objects.all().order_by('priority'),
	           'local_advisory_committee': LocalAdvisoryCommittee.objects.all().order_by('priority'),
	           'symposia'       : Symposia.objects.all(),
	           'carousel_images': Carousel.objects.all(),
	           'programs'       : Program.objects.all(),
	           }
	return render(request, 'home/home.html', context)


def symposia_list(request):
	symposia = Symposia.objects.all()
	return render(request, 'home/symposia.html', {'symposia': symposia})

def speakers(request):
	speakers = Speaker.objects.all().order_by('priority')
	return render(request, 'home/speakers.html', {'speakers': speakers})

def programs(request):
	programs = Program.objects.all()
	return render(request, 'home/programs.html', {'programs': programs})

def registration(request):
	return render(request, 'home/registration.html')

def contact(request):
	return render(request, 'home/contact.html')

def tourist_attractions(request):
	return render(request, 'home/tourist_attractions.html')