from django.contrib import admin

from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user__first_name', 'fee_structure', 'status_code', 'ref_no', 'date']
    search_fields = ['user', 'ref_no']