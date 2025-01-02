from .models import PaperAbstract
from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin



# Register your models here.


class PaperResource(resources.ModelResource):

	def dehydrate_abstract(self, paper):
		return f"https://iconmat2025.cusat.ac.in/media/{paper.abstract}"
	class Meta:
		model = PaperAbstract



@admin.register(PaperAbstract)
class PaperAbstractAdmin(ExportMixin,admin.ModelAdmin):
	list_display = ['title', 'name','phone_number','user_email','title_of_abstract','designation','organization','symposia','abstract','mode_of_presentation']
	list_filter = ['title', 'name','phone_number','title_of_abstract','designation','organization','symposia','abstract','mode_of_presentation']
	search_fields = ['title', 'name','phone_number','title_of_abstract','designation','organization','symposia','abstract','mode_of_presentation']
	resource_classes = [PaperResource]

	def user_email(self, obj):
		return obj.user.email if obj.user else "No User"

	user_email.short_description = "User Email"

