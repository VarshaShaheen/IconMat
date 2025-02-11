from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Participant, CheckIn


class ParticipantResource(resources.ModelResource):
    class Meta:
        model = Participant

@admin.register(Participant)
class ParticipantAdmin(ImportExportModelAdmin):
    list_display = ("iconmat_id", "name", "category","presentation_id","institution","email","registration_id","amount_paid")
    search_fields = ("name","iconmat_id")
    resource_class = ParticipantResource



admin.site.register(CheckIn)