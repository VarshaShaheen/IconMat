from django.forms import ModelForm
from .models import PaperAbstract


class PaperAbstractForm(ModelForm):
	class Meta:
		model = PaperAbstract
		fields = ['title', 'authors','presentation', 'file']