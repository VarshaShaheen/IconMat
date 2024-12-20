import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import threading

from home.utils import send_html_email


# Create your models here.


class FeeDetails(models.Model):
	# Conference Registration Fees
	registration_fee_indian_student_early = models.FloatField(blank=True, null=True)
	registration_fee_indian_faculty_or_research_personal_early = models.FloatField(blank=True, null=True)
	registration_fee_indian_industry_early = models.FloatField(blank=True, null=True)

	registration_fee_indian_student_late = models.FloatField(blank=True, null=True)
	registration_fee_indian_faculty_or_research_personal_late = models.FloatField(blank=True, null=True)
	registration_fee_indian_industry_late = models.FloatField(blank=True, null=True)

	registration_fee_foreign_student_early = models.FloatField(blank=True, null=True)
	registration_fee_foreign_faculty_or_research_personal_early = models.FloatField(blank=True, null=True)
	registration_fee_foreign_industry_early = models.FloatField(blank=True, null=True)

	registration_fee_foreign_student_late = models.FloatField(blank=True, null=True)
	registration_fee_foreign_faculty_or_research_personal_late = models.FloatField(blank=True, null=True)
	registration_fee_foreign_industry_late = models.FloatField(blank=True, null=True)

	# Preconference Registraion Fees
	pre_conference_registration_fee_indian_student_early = models.FloatField(blank=True, null=True)
	pre_conference_registration_fee_indian_faculty_or_research_personal_early = models.FloatField(blank=True, null=True)
	pre_conference_registration_fee_indian_industry_early = models.FloatField(blank=True, null=True)

	pre_conference_registration_fee_indian_student_late = models.FloatField(blank=True, null=True)
	pre_conference_registration_fee_indian_faculty_or_research_personal_late = models.FloatField(blank=True, null=True)
	pre_conference_registration_fee_indian_industry_late = models.FloatField(blank=True, null=True)

	pre_conference_registration_fee_foreign_student_early = models.FloatField(blank=True, null=True)
	pre_conference_registration_fee_foreign_faculty_or_research_personal_early = models.FloatField(blank=True,
	                                                                                               null=True)
	pre_conference_registration_fee_foreign_industry_early = models.FloatField(blank=True, null=True)

	pre_conference_registration_fee_foreign_student_late = models.FloatField(blank=True, null=True)
	pre_conference_registration_fee_foreign_faculty_or_research_personal_late = models.FloatField(blank=True, null=True)
	pre_conference_registration_fee_foreign_industry_late = models.FloatField(blank=True, null=True)

	# Accomodation Fees
	accommodation_foreign_student_single = models.FloatField(blank=True, null=True)
	accommodation_foreign_faculty_or_research_personal_single = models.FloatField(blank=True, null=True)
	accommodation_foreign_industry_single = models.FloatField(blank=True, null=True)

	accommodation_foreign_student_shared = models.FloatField(blank=True, null=True)
	accommodation_foreign_faculty_or_research_personal_shared = models.FloatField(blank=True, null=True)
	accommodation_foreign_industry_shared = models.FloatField(blank=True, null=True)


class FeeStructure(models.Model):
	registration_fee = models.FloatField(blank=True, null=True)
	pre_conference_workshop_fee = models.FloatField(blank=True, null=True)
	accommodation_fee = models.FloatField(blank=True, null=True)
	other_fee = models.FloatField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def total_fee(self):
		return (self.registration_fee if self.registration_fee else 0) + (
			self.pre_conference_workshop_fee if self.pre_conference_workshop_fee else 0) + (
			self.accommodation_fee if self.accommodation_fee else 0) + (self.other_fee if self.other_fee else 0)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return str(self.total_fee())


class Registration(models.Model):
	title_choices = [('Prof', 'Prof'), ('Dr', 'Dr'), ('Mr', 'Mr'), ('Ms', 'Ms'), ]
	country_choices = [('India', 'India'), ('Other', 'Other'), ]
	category_choices = [('Invited Speaker', 'Invited Speaker'),
	                    ('Faculty/Research Personnel/Post Doctoral Fellow', 'Faculty/Research Personnel/Post Doctoral Fellow'), ('Student', 'Student'),
	                    ('Industry', 'Industry'), ]
	accommodation_choices = [('Single Room', 'Single Room'),
	                         ('No Accommodation Required', 'No Accommodation Required'), ]

	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
	title = models.CharField(max_length=50, choices=title_choices)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50, blank=True, null=True)
	email = models.EmailField()
	contact_number = models.CharField(max_length=15)
	affiliation_or_institution = models.CharField(max_length=100)
	designation = models.CharField(max_length=100)
	country = models.CharField(max_length=50, choices=country_choices)
	other_country = models.CharField(max_length=50, blank=True, null=True,
	                                 help_text='Please specify if you selected "Other" in the country field')
	category_of_participant = models.CharField(max_length=50, choices=category_choices,
	                                           help_text='Please select the category')

	conference_registration = models.BooleanField(default=False)
	pre_conference_workshop_registration = models.BooleanField(default=False)

	accommodation_preference = models.CharField(max_length=50, choices=accommodation_choices,
	                                            default='No Accommodation Required')

	fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, blank=True, null=True)

	registration_completed = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	reg_id = models.CharField(max_length=100, blank=True, null=True)

	step = models.IntegerField(default=1)

	class Meta:
		ordering = ('-created_at',)

	def foriegn_delegates(self):
		return True if self.country == 'Other' else False

	def accommodation_required(self):
		return True if self.accommodation_preference != 'No Accommodation Required' else False

	@property
	def full_name(self):
		return f"{self.title}.{self.first_name} {self.last_name}"

	def __str__(self):
		return str(self.title) + str(self.first_name) + str(self.last_name)

	@property
	def raw_mobile_no(self):
		# last 10 digits of the mobile number
		return self.contact_number[-10:]


	def send_email(self, subject, content):
		context = {
			'subject'     : subject,
			'content'     :content,
			'user_name'   : self.full_name,
		}
		threading.Thread(target=send_html_email, args=(context['subject'], self.user.email, context)).start()



@receiver(pre_save, sender=Registration)
def registration_completed(sender, instance, **kwargs):
	if instance.registration_completed and not instance.reg_id:
		instance.reg_id = f"ICO-{instance.user.id}-{instance.id}"


class Currency(models.Model):
	rates = models.JSONField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.created_at.strftime('%d-%m-%Y')