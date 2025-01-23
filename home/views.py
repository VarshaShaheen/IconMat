from django.shortcuts import render
from django.views.generic import TemplateView

from .models import *


def home(request):
    context = {'chairs': People.objects.filter(designation='Conference Chair').order_by('priority'),
               'patrons': People.objects.filter(designation='Conference Patron').order_by('priority'),
               'speakers': Speaker.objects.all().order_by('priority'),
               'advisory_committee': AdvisoryCommittee.objects.all().order_by('priority'),
               'local_advisory_committee': LocalOrganisingCommittiee.objects.all().order_by('priority'),
               'symposia': Symposia.objects.all(),
               'carousel_images': Carousel.objects.all(),
               'programs': Program.objects.all(),
               'dates': Dates.objects.last(),
               'sponsors': Sponsor.objects.all().order_by('-id')
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
    context = {"dates": Dates.objects.last()}
    return render(request, 'home/registration.html', context)


def contact(request):
    return render(request, 'home/contact.html')


def tourist_attractions(request):
    context = {"attractions": TouristAttraction.objects.all()}
    return render(request, 'home/tourist_attractions.html', context)


class Terms(TemplateView):
    template_name = 'home/terms.html'


class Privacy(TemplateView):
    template_name = 'home/privacy.html'


class Refund(TemplateView):
    template_name = 'home/refund.html'


class Disclaimer(TemplateView):
    template_name = 'home/disclaimer.html'
