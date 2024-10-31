from django.contrib import admin

# Register your models here.

from .models import PaperAbstract

@admin.register(PaperAbstract)
class PaperAbstractAdmin(admin.ModelAdmin):
	list_display = ['title', 'authors', 'created_at', 'presentation']
	list_filter = ['created_at', 'presentation']
	search_fields = ['title', 'authors']
	date_hierarchy = 'created_at'
	list_per_page = 20