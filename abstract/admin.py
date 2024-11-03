from django.contrib import admin

# Register your models here.

from .models import PaperAbstract

@admin.register(PaperAbstract)
class PaperAbstractAdmin(admin.ModelAdmin):
	list_display = ['title', 'name','phone_number','title_of_abstract','designation','organization','symposia','abstract','mode_of_presentation']
	list_filter = ['title', 'name','phone_number','title_of_abstract','designation','organization','symposia','abstract','mode_of_presentation']
	search_fields = ['title', 'name','phone_number','title_of_abstract','designation','organization','symposia','abstract','mode_of_presentation']