from django.contrib import admin
from .models import Registration, FeeDetails, FeeStructure
from import_export import resources
from import_export.admin import ExportMixin
from import_export import resources, fields
from import_export.widgets import CharWidget

# Register your models here.


class RegistrationResource(resources.ModelResource):
	fee_structure = fields.Field(attribute='fee_structure', column_name='Fee Structure', widget=CharWidget())
	class Meta:
		model = Registration

@admin.register(Registration)
class RegistrationAdmin(ExportMixin,admin.ModelAdmin):
	list_display = ['title', 'first_name', 'last_name', 'email', 'contact_number', 'affiliation_or_institution', 'designation', 'country', 'category_of_participant', 'registration_completed', 'created_at']
	search_fields = ['title', 'first_name', 'last_name', 'email', 'contact_number', 'affiliation_or_institution', 'designation', 'country', 'category_of_participant']
	list_filter = ['country', 'category_of_participant', 'registration_completed']
	# list_editable = ['registration_completed']
	list_display_links = ['title','first_name', 'last_name']
	list_select_related = ['fee_structure']
	date_hierarchy = 'created_at'
	ordering = ['-created_at']
	# actions = ['mark_as_completed']
	resource_classes = [RegistrationResource]

	# def mark_as_completed(self, request, queryset):
	# 	queryset.update(registration_completed=True)
	# 	self.message_user(request, 'Selected registrations have been marked as completed.')
	# mark_as_completed.short_description = 'Mark selected registrations as completed'


admin.site.register(FeeDetails)
admin.site.register(FeeStructure)