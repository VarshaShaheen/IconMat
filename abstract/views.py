from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PaperAbstractForm


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
				abstract.send_email()

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
