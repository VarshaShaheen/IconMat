from django.shortcuts import render
from django.views.generic import TemplateView
from collections import defaultdict


from .models import *


def home(request):
    sponsors = Sponsor.objects.all()
    sponsors_by_category = {
        "GVT FND": [],
        "GOLD": [],
        "SILVER": [],
    }

    # Group sponsors into categories
    for sponsor in sponsors:
        sponsors_by_category.setdefault(sponsor.category, []).append(sponsor)

    # Include other categories if necessary
    sponsors_by_category["OTHER"] = [
        s for s in sponsors if s.category not in sponsors_by_category
    ]

    context = {'chairs': People.objects.filter(designation='Conference Chair').order_by('priority'),
               'patrons': People.objects.filter(designation='Conference Patron').order_by('priority'),
               'speakers': Speaker.objects.all().order_by('priority'),
               'advisory_committee': AdvisoryCommittee.objects.all().order_by('priority'),
               'local_advisory_committee': LocalOrganisingCommittiee.objects.all().order_by('priority'),
               'symposia': Symposia.objects.all(),
               'carousel_images': Carousel.objects.all(),
               'programs': Program.objects.all(),
               'dates': Dates.objects.last(),
               'sponsors_by_category': dict(sponsors_by_category)
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
