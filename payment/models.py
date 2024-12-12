from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.


class Payment(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	registration = models.ForeignKey('registration.Registration', on_delete=models.CASCADE, related_name='payments')
	fee_structure = models.ForeignKey('registration.FeeStructure', on_delete=models.CASCADE)
	status_code = models.CharField(max_length=10, blank=True, null=True)
	payment_request_data = models.JSONField(blank=True, null=True)
	gateway_responce_data = models.JSONField(blank=True, null=True)
	ref_no = models.CharField(max_length=100, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.ref_no}"

	@property
	def pg_amount(self):
		return str(self.fee_structure.total_fee())


@receiver(pre_save, sender=Payment)
def set_ref_no(sender, instance, **kwargs):
	if not instance.ref_no:
		timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
		unique_id = uuid.uuid4().hex[:6].upper()
		instance.ref_no = f"PAY-{instance.registration.id}-{instance.user.id}-{timestamp}-{unique_id}"
