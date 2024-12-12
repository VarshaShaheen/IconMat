import hashlib

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from registration.models import Registration
from django.shortcuts import get_object_or_404
import json

from .models import Payment

# AES Key (16 bytes for AES-128)
# AES_KEY = b"1400012609205020"  # Replace with your encryption key


AES_KEY = b"3819510767701000"  # Replace with your encryption key


def encrypt_data(data):
	"""Encrypt data using AES ECB mode with PKCS7 padding."""
	from Crypto.Cipher import AES
	from Crypto.Util.Padding import pad
	import base64

	data_bytes = data.encode('utf-8')
	cipher = AES.new(AES_KEY, AES.MODE_ECB)
	padded_data = pad(data_bytes, AES.block_size)

	# Encrypt the data
	encrypted = cipher.encrypt(padded_data)

	# Encode the encrypted data as base64 to make it a readable string
	return base64.b64encode(encrypted).decode('utf-8')


def validate_hash(rs, *args):
	# Construct the input string from positional arguments
	hash_input = "|".join(str(arg) for arg in args) + f"|{AES_KEY.decode()}"
	print("Hash Input:", hash_input)

	# Generate the hash
	expected_hash = hashlib.sha512(hash_input.encode()).hexdigest()

	# Return comparison result
	return rs == expected_hash

def prepare_payment_data(payment):
	# Replace with actual transaction details

	mandatory_fields = f"{payment.ref_no}|45|{0.0}"
	optional_fields = f"icONMAT 2025|{payment.registration.full_name}|{payment.registration.category_of_participant}|{payment.fee_structure.registration_fee}|{payment.fee_structure.pre_conference_workshop_fee}|{payment.fee_structure.accommodation_fee}|Processing|{payment.registration.raw_mobile_no}"
	return_url = "http://localhost:8000/payment/process/"
	reference_no = f"{payment.ref_no}"
	sub_merchant_id = "45"
	transaction_amount = f"{payment.pg_amount}"
	pay_mode = "9"

	# mandatory_fields = f"{payment.ref_no}|45|10|26/NOV/2024"
	# optional_fields = "x|test@gmail.com|9876543210|x|x"
	# # return_url = "http://localhost:8000/payment/process/"
	# return_url = "https://iconmat2025.cusat.ac.in/payment/process/"
	# reference_no = f"{payment.ref_no}"
	# sub_merchant_id = "45"
	# transaction_amount = "10"
	# pay_mode = "9"

	payment_data = {
		"mandatoryFields"  : mandatory_fields,
		"optionalFields"   : optional_fields,
		"returnURL"        : return_url,
		"referenceNo"      : reference_no,
		"subMerchantId"    : sub_merchant_id,
		"transactionAmount": transaction_amount,
		"payMode"          : pay_mode

	}

	encrypted_payment_data = {
		"mandatoryFields"  : encrypt_data(mandatory_fields),
		"optionalFields"   : encrypt_data(optional_fields),
		"returnURL"        : encrypt_data(return_url),
		"referenceNo"      : encrypt_data(reference_no),
		"subMerchantId"    : encrypt_data(sub_merchant_id),
		"transactionAmount": encrypt_data(transaction_amount),
		"payMode"          : encrypt_data(pay_mode)
	}

	return [payment_data, encrypted_payment_data]


def initiate_payment(request):
	context = {'registration': get_object_or_404(Registration, user=request.user)}

	payment = Payment.objects.create(user=request.user, registration=context['registration'],
	                                 fee_structure=context['registration'].fee_structure)
	payment_data, encrypted_payment_data = prepare_payment_data(payment)
	payment.payment_request_data = json.dumps(payment_data)
	payment.save()

	# Add the payment data to the context
	print("Reference No: ", payment.ref_no)
	context.update(encrypted_payment_data)
	context['merchantid'] = 386778 #real
	# context['merchantid'] = 140921 #test
	print(context)

	return render(request, "payment/initiate_payment.html", context)


@csrf_exempt
def process_payment(request):
	if request.method == "POST":
		# Log raw data for debugging
		# print("Raw Data:", request.POST)
		print("\n", request.POST.get("ReferenceNo"))
		payment = get_object_or_404(Payment,ref_no__exact=request.POST.get("ReferenceNo"))
		# payment = Payment.objects.last()
		payment.gateway_responce_data = json.dumps(request.POST.dict())
		payment.save()

		print(payment.payment_request_data, "\n", payment.gateway_responce_data)

		# Extract fields from the POST data
		rs = request.POST.get("RS")
		res_id = request.POST.get("ID")
		response_code = request.POST.get("Response Code")
		ref_no = request.POST.get("Unique Ref Number")  # Use 'ReferenceNo' instead of 'Reference No' for consistency
		service_tax_amount = request.POST.get("Service Tax Amount")
		processing_fee = request.POST.get("Processing Fee Amount")
		total_amount = request.POST.get("Total Amount")
		transaction_amount = request.POST.get("Transaction Amount")
		transaction_date = request.POST.get("Transaction Date")
		intercharge_value = request.POST.get("Interchange Value")
		tdr = request.POST.get("TDR")
		payment_mode = request.POST.get("Payment Mode")
		submerchant_id = request.POST.get("SubMerchantId")
		ref_no_2 = request.POST.get("ReferenceNo")
		tps = request.POST.get("TPS")

		payment.status_code = response_code
		payment.save()

		if validate_hash(rs, res_id, response_code, ref_no, service_tax_amount, processing_fee, total_amount,
		                 transaction_amount, transaction_date, intercharge_value, tdr, payment_mode, submerchant_id,
		                 ref_no_2, tps):
			# response_code = 'E000'  # For testing purposes
			if response_code == 'E000':  # Payment Success
				payment.registration.registration_completed = True
				payment.registration.save()
				return redirect('registration_completed', ref_no_2)
			else:  # Payment Failed
				payment.registration.registration_completed = False
				payment.registration.save()

				print("Payment failed")
				return redirect('registration_failed', ref_no_2)

		else:
			print("Hash validation failed")
			return redirect('registration_failed',ref_no_2)

	return JsonResponse({"error": "Invalid request method"}, status=405)


def handle_payment_status(request):
	return HttpResponse("Payment Status Page")
