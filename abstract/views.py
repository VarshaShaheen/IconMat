from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView
import logging

from home.models import Dates
from .models import PaperAbstract

from .forms import PaperAbstractForm, FullPaperForm

logger = logging.getLogger(__name__)


@login_required
def abstract_submission(request):
	form = PaperAbstractForm()

	if request.method == 'POST':
		form = PaperAbstractForm(request.POST, request.FILES)

		if form.is_valid():
			try:
				# Save abstract and associate it with the current user
				abstract = form.save(commit=False)
				abstract.user = request.user
				abstract.save()

				# Attempt to send the confirmation email
				try:
					abstract.send_email()
				except Exception as e:

					logger.error(f"Error sending email: {e}")
					messages.error(request,
					               'There was an error sending the confirmation email. Please contact the administrator.')
					return render(request, 'others/notification.html', {
						'message': "There was an error sending the confirmation email. Please contact the administrator"})
				# Success message
				return render(request, 'others/notification.html', {'message': "Abstract submitted successfully!"})

			except Exception as e:
				# Log the exception if needed
				# logger.error(f"Error submitting abstract: {e}")

				# Show error message to user
				messages.error(request, 'There was an error processing your submission. Please try again later.')
		else:
			messages.error(request, 'Please correct the errors in the form.')

	# Render form page with any messages
	return render(request, 'abstract/abstract_submission.html', {'form': form})


class AbstractDetail(TemplateView):
	template_name = 'abstract/abstract_details.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['dates'] = Dates.objects.last()
		return context


class FullPaperDetails(TemplateView):
	template_name = 'abstract/full_paper_details.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['dates'] = Dates.objects.last()
		return context


@login_required
def view_abstract(request):
	abstracts = PaperAbstract.objects.filter(user=request.user)
	return render(request, 'abstract/view_abstracts.html', {'abstracts': abstracts})


@login_required
def full_paper_submission(request):
	form = FullPaperForm(user = request.user)

	if request.method == 'POST':
		form = FullPaperForm(request.POST, request.FILES,user = request.user)

		if form.is_valid():
			try:
				# Save abstract and associate it with the current user
				manuscript = form.save(commit=False)
				manuscript.user = request.user
				manuscript.save()

				# Attempt to send the confirmation email
				try:
					manuscript.send_email()
				except Exception as e:

					logger.error(f"Error sending email: {e}")
					messages.error(request,
					               'There was an error sending the confirmation email. Please contact the administrator.')
					return render(request, 'others/notification.html', {
						'message': "There was an error sending the confirmation email. Please contact the administrator"})
				# Success message
				return render(request, 'others/notification.html', {'message': "Full Paper submitted successfully!"})

			except Exception as e:
				# Log the exception if needed
				# logger.error(f"Error submitting abstract: {e}")

				# Show error message to user
				messages.error(request, 'There was an error processing your submission. Please try again later.')
		else:
			messages.error(request, 'Please correct the errors in the form.')

	# Render form page with any messages
	return render(request, 'abstract/full_paper_submission.html', {'form': form})
