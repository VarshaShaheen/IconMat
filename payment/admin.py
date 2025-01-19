from django.contrib import admin

from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'fee_structure', 'status_code', 'ref_no', 'date']
    search_fields = ['ref_no']