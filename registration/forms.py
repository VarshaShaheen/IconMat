from django import forms
from django.core.exceptions import ValidationError

from .models import Registration


class BasicInfoForm(forms.ModelForm):
	class Meta:
		model = Registration
		fields = ['title', 'first_name', 'last_name', 'email', 'contact_number', 'affiliation_or_institution','department',
		          'designation', 'country', 'other_country', 'category_of_participant', ]

	def __init__(self, *args, **kwargs):
		instance = kwargs.get('instance')
		super().__init__(*args, **kwargs)
		if instance and instance.user:
			print(f"Pre-filling form: {instance.user.first_name}, {instance.user.last_name}, {instance.user.email}")
			self.initial['first_name'] = instance.user.first_name.split(' ')[0]
			self.initial['last_name'] = " ".join(instance.user.first_name.split(' ')[1:]) if len(instance.user.first_name.split(' ')) > 1 else ''
			self.initial['email'] = instance.user.email


class ConferenceInfoForm(forms.ModelForm):
	class Meta:
		model = Registration
		fields = ['conference_registration', 'pre_conference_workshop_registration', ]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Make both fields optional initially
		self.fields['conference_registration'].required = False
		self.fields['pre_conference_workshop_registration'].required = False

	def clean(self):
		cleaned_data = super().clean()
		conference_registration = cleaned_data.get('conference_registration')
		pre_conference_workshop_registration = cleaned_data.get('pre_conference_workshop_registration')

		# Ensure that at least one of the fields is filled
		if not conference_registration and not pre_conference_workshop_registration:
			raise ValidationError('At least one of the fields must be filled.')

		return cleaned_data


class AdditionalInfoForm(forms.ModelForm):
	class Meta:
		model = Registration
		fields = []  # Start with an empty list; we'll add fields dynamically

	def __init__(self, *args, **kwargs):
		instance = kwargs.get('instance')  # Retrieve the instance
		super().__init__(*args, **kwargs)

		# Check if an instance is provided and if accommodation is required
		if instance and instance.foriegn_delegates():
			self.fields['accommodation_preference'] = forms.ChoiceField(
				choices=Registration.accommodation_choices,
				label="Accommodation Preference",
				widget=forms.Select(attrs={"class": "form-control"}),
				required=False,  # Make this field optional if needed
			)

			if instance.accommodation_preference:
				self.fields['accommodation_preference'].initial = instance.accommodation_preference
			else:
				self.fields['accommodation_preference'].initial = Registration.accommodation_preference

	def save(self, commit=True):
		instance = super().save(commit=False)  # Don't commit yet; handle the extra field

		# Check if accommodation_preference exists in cleaned data and save it
		accommodation_preference = self.cleaned_data.get('accommodation_preference', None)
		if accommodation_preference is not None:
			instance.accommodation_preference = accommodation_preference
			print("Accommodation Preference: ", instance.accommodation_preference)
		else:
			# If not set, assign a default value or leave it empty
			instance.accommodation_preference = "No Accommodation Required"
			print("Accommodation Preference not set: ", instance.accommodation_preference)

		if commit:
			instance.save()
		return instance
