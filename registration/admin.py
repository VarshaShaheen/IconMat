from django.contrib import admin
from .models import Registration, FeeDetails, FeeStructure


# Register your models here.


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
	list_display = ['title', 'first_name', 'last_name', 'email', 'contact_number', 'affiliation_or_institution', 'designation', 'country', 'category_of_participant', 'registration_completed', 'created_at']
	search_fields = ['title', 'first_name', 'last_name', 'email', 'contact_number', 'affiliation_or_institution', 'designation', 'country', 'category_of_participant']
	list_filter = ['country', 'category_of_participant', 'registration_completed']
	# list_editable = ['registration_completed']
	list_display_links = ['title','first_name', 'last_name']
	list_select_related = ['fee_structure']
	date_hierarchy = 'created_at'
	ordering = ['-created_at']
	# actions = ['mark_as_completed']

	# def mark_as_completed(self, request, queryset):
	# 	queryset.update(registration_completed=True)
	# 	self.message_user(request, 'Selected registrations have been marked as completed.')
	# mark_as_completed.short_description = 'Mark selected registrations as completed'


admin.site.register(FeeDetails)
admin.site.register(FeeStructure)