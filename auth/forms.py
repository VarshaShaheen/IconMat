# forms.py
from django import forms
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
	name = forms.CharField(max_length=150, label="Name")

	def save(self, request):
		user = super(CustomSignupForm, self).save(request)
		user.first_name = self.cleaned_data.get('name')
		user.save()
		return user
