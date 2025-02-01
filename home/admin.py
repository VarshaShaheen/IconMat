from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(People)
admin.site.register(Symposia)
admin.site.register(Program)
admin.site.register(Speaker)
admin.site.register(TechnicalSession)

admin.site.register(Social)
admin.site.register(AdvisoryCommittee)
admin.site.register(LocalOrganisingCommittiee)
admin.site.register(Notification)
admin.site.register(Dates)
admin.site.register(TouristAttraction)
admin.site.register(Sponsor)


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
	pass
