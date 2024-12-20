import threading

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from home.utils import send_html_email
from payment.models import Payment
from .forms import *
import requests
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import Registration, FeeDetails, FeeStructure, Currency


@login_required
def basic_info(request):
	registration, created = Registration.objects.get_or_create(user=request.user)
	if not registration.registration_completed:
		context = {
			'registration': registration,
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
		return redirect('registration_completed')


@login_required
def conference_info(request):
	# Fetch or create a Registration object for the user
	registration, created = Registration.objects.get_or_create(user=request.user)
	if not registration.registration_completed:
		context = {
			'registration': registration,
			'current_step': registration.step,
			'total_steps' : 4
		}

		if request.method == 'POST':
			form = ConferenceInfoForm(request.POST, instance=registration)
			if form.is_valid():
				# Save the form
				reg = form.save(commit=False)
				reg.step = 4
				reg.save()
				if reg.foriegn_delegates():
					reg.step = 3
					reg.save()
					return redirect('additional_info')
				else:
					return redirect('review_and_payment')
			context['form'] = form

		else:
			# Pre-fill the form with existing data
			form = ConferenceInfoForm(instance=registration)
			context['form'] = form

		return render(request, 'registration/conference_info.html', context)
	else:
		return redirect('registration_completed')


@login_required
def additional_info(request):
	registration, created = Registration.objects.get_or_create(user=request.user)
	if not registration.registration_completed:
		context = {
			'registration': registration,
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
		return redirect('registration_completed')


@login_required
def review_and_payment(request):
	registration, created = Registration.objects.get_or_create(user=request.user)
	if not registration.registration_completed:
		registration_fee, pre_conference_reg_fee, accommodation_fee = calculate_payment(registration)
		if registration.fee_structure:
			print("Updating Fee Structure", registration.fee_structure)
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
		rate = usd_to_inr(1)
		converted_rates = {'registration_fee_usd'      : round(registration_fee / rate, 2),
		                   'pre_conference_reg_fee_usd': round(pre_conference_reg_fee / rate, 2),
		                   'accommodation_fee_usd'     : round(accommodation_fee / rate, 2),
		                   'total_fee_usd'             : round((registration_fee + pre_conference_reg_fee + accommodation_fee) / rate, 2),}
		context = {'current_step'   : registration.step, 'total_steps': 4, 'registration': registration,
		           'converted_rates': converted_rates}

		return render(request, 'registration/review_and_payment.html', context)

	else:
		return redirect('registration_completed')


@login_required
def registration_completed(request, pay_ref_no=None):
	registration, created = Registration.objects.get_or_create(user=request.user)
	payment = Payment.objects.filter(ref_no=pay_ref_no).last()
	if not pay_ref_no:
		payment = Payment.objects.filter(registration=registration, status_code='E000').last()
	if not payment:
		raise Http404("Payment does not exist")

	context = {'registration': registration,
	           'payment'     : payment, }

	if registration.registration_completed:
		return render(request, 'registration/registration_completed.html', context)
	else:
		return redirect('basic_info')


@login_required
def registration_failed(request, pay_ref_no):
	registration, created = Registration.objects.get_or_create(user=request.user)
	payment = get_object_or_404(Payment, ref_no=pay_ref_no)
	context = {'registration': registration,
	           'payment'     : payment, }
	return render(request, 'registration/registration_failed.html', context)


def calculate_payment(registration):
	fee_details = FeeDetails.objects.first()
	# Calculate the registration fee based on the category of the participant
	registration_fee, pre_conference_reg_fee, accommodation_fee = [0, 0, 0]
	early = True

	# Early Registration Fee for Indian Participants (Early)
	if early and not registration.foriegn_delegates():
		if registration.category_of_participant == 'Student':
			registration_fee = fee_details.registration_fee_indian_student_early
			pre_conference_reg_fee = fee_details.pre_conference_registration_fee_indian_student_early
		elif registration.category_of_participant == 'Faculty/Research Personnel/Post Doctoral Fellow' or registration.category_of_participant == 'Invited Speaker':
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
		elif registration.category_of_participant == 'Faculty/Research Personnel/Post Doctoral Fellow' or registration.category_of_participant == 'Invited Speaker':
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
			registration_fee = usd_to_inr(fee_details.registration_fee_foreign_student_early)
			pre_conference_reg_fee = usd_to_inr(fee_details.pre_conference_registration_fee_foreign_student_early)
		elif registration.category_of_participant == 'Faculty/Research Personnel/Post Doctoral Fellow' or registration.category_of_participant == 'Invited Speaker':
			registration_fee = usd_to_inr(fee_details.registration_fee_foreign_faculty_or_research_personal_early)
			pre_conference_reg_fee = usd_to_inr(
				fee_details.pre_conference_registration_fee_foreign_faculty_or_research_personal_early)
		elif registration.category_of_participant == 'Industry':
			registration_fee = usd_to_inr(fee_details.registration_fee_foreign_industry_early)
			pre_conference_reg_fee = usd_to_inr(fee_details.pre_conference_registration_fee_foreign_industry_early)
		else:
			registration_fee = 0
			pre_conference_reg_fee = 0
	# Late Registration Fee for Foriegn Participants
	if not early and registration.foriegn_delegates():
		if registration.category_of_participant == 'Student':
			registration_fee = usd_to_inr(fee_details.registration_fee_foreign_student_late)
			pre_conference_reg_fee = usd_to_inr(fee_details.pre_conference_registration_fee_foreign_student_late)
		elif registration.category_of_participant == 'Faculty/Research Personnel/Post Doctoral Fellow' or registration.category_of_participant == 'Invited Speaker':
			registration_fee = usd_to_inr(fee_details.registration_fee_foreign_faculty_or_research_personal_late)
			pre_conference_reg_fee = usd_to_inr(
				fee_details.pre_conference_registration_fee_foreign_faculty_or_research_personal_late)
		elif registration.category_of_participant == 'Industry':
			registration_fee = usd_to_inr(fee_details.registration_fee_foreign_industry_late)
			pre_conference_reg_fee = usd_to_inr(fee_details.pre_conference_registration_fee_foreign_industry_late)
		else:
			registration_fee = 0
			pre_conference_reg_fee = 0

	if registration.accommodation_required() and registration.foriegn_delegates():
		if registration.category_of_participant == 'Student' and registration.accommodation_preference == 'Single Room':
			accommodation_fee = usd_to_inr(fee_details.accommodation_foreign_student_single)
		elif (
				registration.category_of_participant == 'Faculty/Research Personnel/Post Doctoral Fellow' or registration.category_of_participant == 'Invited Speaker') and (
				registration.accommodation_preference == 'Single Room'):
			accommodation_fee = usd_to_inr(fee_details.accommodation_foreign_faculty_or_research_personal_single)
		elif registration.category_of_participant == 'Industry' and registration.accommodation_preference == 'Single Room':
			accommodation_fee = usd_to_inr(fee_details.accommodation_foreign_industry_single)

		if registration.category_of_participant == 'Student' and registration.accommodation_preference == 'Shared Room':
			accommodation_fee = usd_to_inr(fee_details.accommodation_foreign_student_shared)
		elif (
				registration.category_of_participant == 'Faculty/Research Personnel/Post Doctoral Fellow' or registration.category_of_participant == 'Invited Speaker') and (
				registration.accommodation_preference == 'Shared Room'):
			accommodation_fee = usd_to_inr(fee_details.accommodation_foreign_faculty_or_research_personal_shared)
		elif registration.category_of_participant == 'Industry' and registration.accommodation_preference == 'Shared Room':
			accommodation_fee = usd_to_inr(fee_details.accommodation_foreign_industry_shared)
	else:
		accommodation_fee = 0

	return [registration_fee if registration.conference_registration else 0, \
	        pre_conference_reg_fee if registration.pre_conference_workshop_registration else 0, \
	        accommodation_fee]


def make_event_ticket():
	# Create a ticket for the event
	pass


def usd_to_inr(usd):
	response = requests.get('https://v6.exchangerate-api.com/v6/b5fbb70e3bacbe3fecaa895b/latest/USD')
	if response.status_code == 200:
		try:
			data = Currency.objects.create(rates=response.json())
		except Exception as e:
			print("Failed to save exchange rate")
			data = Currency.objects.last()
		print(data)
		inr = usd * data.rates['conversion_rates']['INR']
	else:
		print("Failed to fetch exchange rate")
		data = Currency.objects.last()
		inr = usd * data.rates['conversion_rates']['INR']
	return float(round(inr, 2))
