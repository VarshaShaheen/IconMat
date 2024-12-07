from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import Registration, FeeDetails, FeeStructure


@login_required
def basic_info(request):
	registration, created = Registration.objects.get_or_create(user=request.user)
	if not registration.registration_completed:
		context = {
			'current_step': registration.step,
			'total_steps' : 4
		}

		if request.method == 'POST':
			form = BasicInfoForm(request.POST, instance=registration)
			if form.is_valid():
				# Save the form
				reg = form.save(commit=False)
				reg.step = 2
				reg.save()
				return redirect('conference_info')  # Redirect to the next step
			context['form'] = form
		else:
			# Pre-fill the form with existing data
			form = BasicInfoForm(instance=registration)
			context['form'] = form

		return render(request, 'registration/basic_info.html', context)
	else:
		return redirect('registration_complete')


@login_required
def conference_info(request):
	# Fetch or create a Registration object for the user
	registration, created = Registration.objects.get_or_create(user=request.user)
	if not registration.registration_completed:
		context = {
			'current_step': registration.step,
			'total_steps' : 4
		}

		if request.method == 'POST':
			form = ConferenceInfoForm(request.POST, instance=registration)
			if form.is_valid():
				# Save the form
				reg = form.save(commit=False)
				reg.step = 3
				reg.save()
				return redirect('additional_info')
			context['form'] = form

		else:
			# Pre-fill the form with existing data
			form = ConferenceInfoForm(instance=registration)
			context['form'] = form

		return render(request, 'registration/conference_info.html', context)
	else:
		return redirect('registration_complete')


def additional_info(request):
	registration, created = Registration.objects.get_or_create(user=request.user)
	if not registration.registration_completed:
		context = {
			'current_step': registration.step,
			'total_steps' : 4
		}

		if request.method == 'POST':
			form = AdditionalInfoForm(request.POST, instance=registration)
			if form.is_valid():
				reg = form.save(commit=False)
				reg.step = 4  # Update the step to the next one
				reg.save()
				return redirect('review_and_payment')
			else:
				print("Form Errors:", form.errors)  # Debug form errors
			context['form'] = form
		else:
			form = AdditionalInfoForm(instance=registration)
			context['form'] = form

		return render(request, 'registration/additional_info.html', context)
	else:
		return redirect('registration_complete')


def review_and_payment(request):
	registration, created = Registration.objects.get_or_create(user=request.user)
	if not registration.registration_completed:
		registration_fee, pre_conference_reg_fee, accommodation_fee = calculate_payment(registration)
		if registration.fee_structure:
			# Update the existing FeeStructure
			fee_structure = registration.fee_structure
			fee_structure.registration_fee = registration_fee
			fee_structure.pre_conference_workshop_fee = pre_conference_reg_fee
			fee_structure.accommodation_fee = accommodation_fee
			fee_structure.save()
		else:
			# Create a new FeeStructure and associate it
			fee_structure = FeeStructure.objects.create(
				registration_fee=registration_fee,
				pre_conference_workshop_fee=pre_conference_reg_fee,
				accommodation_fee=accommodation_fee,
			)
			registration.fee_structure = fee_structure
			registration.save()
		context = {'current_step': registration.step, 'total_steps': 4, 'registration': registration, }

		return render(request, 'registration/review_and_payment.html', context)

	else:
		return redirect('registration_complete')


def calculate_payment(registration):
	fee_details = FeeDetails.objects.first()
	# Calculate the registration fee based on the category of the participant
	early = True

	# Early Registration Fee for Indian Participants (Early)
	if early and not registration.foriegn_delegates():
		if registration.category_of_participant == 'Student':
			registration_fee = fee_details.registration_fee_indian_student_early
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_indian_student_early
		elif registration.category_of_participant == 'Faculty/Research Personnel' or registration.category_of_participant == 'Invited Speaker':
			registration_fee = fee_details.registration_fee_indian_faculty_or_research_personal_early
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_indian_faculty_or_research_personal_early
		elif registration.category_of_participant == 'Industry':
			registration_fee = fee_details.registration_fee_indian_industry_early
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_indian_industry_early
		else:
			registration_fee = 0
			pre_conference_reg_fee = 0

	# Late Registration Fee for Indian Participants (Early)
	if not early and not registration.foriegn_delegates():
		if registration.category_of_participant == 'Student':
			registration_fee = fee_details.registration_fee_indian_student_late
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_indian_student_late
		elif registration.category_of_participant == 'Faculty/Research Personnel' or registration.category_of_participant == 'Invited Speaker':
			registration_fee = fee_details.registration_fee_indian_faculty_or_research_personal_late
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_indian_faculty_or_research_personal_late
		elif registration.category_of_participant == 'Industry':
			registration_fee = fee_details.registration_fee_indian_industry_late
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_indian_industry_late
		else:
			registration_fee = 0
			pre_conference_reg_fee = 0

	# Early Registration Fee for Foriegn Participants (Early)
	if early and registration.foriegn_delegates():
		if registration.category_of_participant == 'Student':
			registration_fee = fee_details.registration_fee_foreign_student_early
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_foreign_student_early
		elif registration.category_of_participant == 'Faculty/Research Personnel' or registration.category_of_participant == 'Invited Speaker':
			registration_fee = fee_details.registration_fee_foreign_faculty_or_research_personal_early
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_foreign_faculty_or_research_personal_early
		elif registration.category_of_participant == 'Industry':
			registration_fee = fee_details.registration_fee_foreign_industry_early
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_foreign_industry_early
		else:
			registration_fee = 0
			pre_conference_reg_fee = 0
	# Late Registration Fee for Foriegn Participants (Early)
	if not early and registration.foriegn_delegates():
		if registration.category_of_participant == 'Student':
			registration_fee = fee_details.registration_fee_foreign_student_late
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_foreign_student_late
		elif registration.category_of_participant == 'Faculty/Research Personnel' or registration.category_of_participant == 'Invited Speaker':
			registration_fee = fee_details.registration_fee_foreign_faculty_or_research_personal_late
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_foreign_faculty_or_research_personal_late
		elif registration.category_of_participant == 'Industry':
			registration_fee = fee_details.registration_fee_foreign_industry_late
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_foreign_industry_late
		else:
			registration_fee = 0
			pre_conference_reg_fee = 0

	if registration.accommodation_required() and registration.foriegn_delegates():
		if registration.category_of_participant == 'Student' and registration.accommodation_preference == 'Single Room':
			accommodation_fee = fee_details.accommodation_foreign_student_single
		elif (
				registration.category_of_participant == 'Faculty/Research Personnel' or registration.category_of_participant == 'Invited Speaker') and (
				registration.accommodation_preference == 'Single Room'):
			accommodation_fee = fee_details.accommodation_foreign_faculty_or_research_personal_single
		elif registration.category_of_participant == 'Industry' and registration.accommodation_preference == 'Single Room':
			accommodation_fee = fee_details.accommodation_foreign_industry_single

		if registration.category_of_participant == 'Student' and registration.accommodation_preference == 'Shared Room':
			accommodation_fee = fee_details.accommodation_foreign_student_shared
		elif (
				registration.category_of_participant == 'Faculty/Research Personnel' or registration.category_of_participant == 'Invited Speaker') and (
				registration.accommodation_preference == 'Shared Room'):
			accommodation_fee = fee_details.accommodation_foreign_faculty_or_research_personal_shared
		elif registration.category_of_participant == 'Industry' and registration.accommodation_preference == 'Shared Room':
			accommodation_fee = fee_details.accommodation_foreign_industry_shared
	else:
		accommodation_fee = 0

	return [registration_fee, pre_conference_reg_fee, accommodation_fee]


def registration_completed(request):
	# send email
	# make event ticket


	return render(request, 'registration/registration_completed.html')


def make_event_ticket():
	# Create a ticket for the event
	pass
