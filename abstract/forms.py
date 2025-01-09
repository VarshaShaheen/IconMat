from django import forms
from django.forms import ModelForm
from .models import PaperAbstract, FullPaper


class PaperAbstractForm(ModelForm):
	mode_of_presentation = forms.ChoiceField(choices=[('poster', 'Poster Presentation')],initial='poster')
	class Meta:
		model = PaperAbstract
		fields = ['title', 'name', 'designation', 'phone_number', 'title_of_abstract', 'organization', 'symposia',
		          'abstract', 'mode_of_presentation']

		description = "Please fill out the form below to submit your abstract. All fields are required."
		help_texts = {
			'phone_number': 'Phone Number (with country code)',
		}


class FullPaperForm(ModelForm):
	class Meta:
		model = FullPaper
		fields = ['abstract', 'title_of_manuscript', 'institution', 'manuscript']

		description = "Please fill out the form below to submit your manuscript. All fields are required."
		help_texts = {
			'abstract': 'Select your submitted abstract',
		}

	def __init__(self,*args,**kwargs):
		user = kwargs.pop('user', None)
		print(f"Filtering abstracts for user: {user}")
		super().__init__(*args, **kwargs)
		if user:
			self.fields['abstract'].queryset = PaperAbstract.objects.filter(user=user)