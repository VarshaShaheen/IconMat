from django.forms import ModelForm
from .models import PaperAbstract


class PaperAbstractForm(ModelForm):
	class Meta:
		model = PaperAbstract
		fields = ['title', 'name', 'designation', 'phone_number', 'title_of_abstract', 'organization', 'symposia',
		          'abstract', 'mode_of_presentation']

		description = "Please fill out the form below to submit your abstract. All fields are required."
		help_texts = {
			'phone_number': 'Phone Number (with country code)',
		}
