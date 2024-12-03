from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Payment(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	registration = models.ForeignKey('registration.Registration', on_delete=models.CASCADE)
	fee_structure = models.ForeignKey('registration.FeeStructure', on_delete=models.CASCADE)
	status_code = models.CharField(max_length=10, blank=True, null=True)
	payment_request_data = models.JSONField(blank=True, null=True)

