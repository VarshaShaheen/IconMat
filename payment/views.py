import hashlib

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from registration.models import Registration
from django.shortcuts import get_object_or_404
import json

from .models import Payment

# AES Key (16 bytes for AES-128)
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


def prepare_payment_data(registration, fee_structure):
	# Replace with actual transaction details
	print(fee_structure, registration)
	mandatory_fields = "123abc|45|10"
	optional_fields = "x|x|x|0|0|0|x|9876543210"
	return_url = "http://localhost:8000/payment/process/"
	reference_no = "123abc"
	sub_merchant_id = "45"
	transaction_amount = "10"
	pay_mode = "9"

	return {
		"mandatoryFields"  : encrypt_data(mandatory_fields),
		"optionalFields"   : encrypt_data(optional_fields),
		"returnURL"        : encrypt_data(return_url),
		"referenceNo"      : encrypt_data(reference_no),
		"subMerchantId"    : encrypt_data(sub_merchant_id),
		"transactionAmount": encrypt_data(transaction_amount),
		"payMode"          : encrypt_data(pay_mode)
	}


def initiate_payment(request):
	context = {'registration': get_object_or_404(Registration, user=request.user)}

	payment_data = prepare_payment_data(context['registration'], context['registration'].fee_structure)
	payment, created = Payment.objects.get_or_create(user=request.user, registration=context['registration'],
	                                                 fee_structure=context['registration'].fee_structure,
	                                                 payment_request_data=json.dumps(payment_data))

	# Add the payment data to the context
	context.update(payment_data)
	context['merchantid'] = 386778
	print(context)

	return render(request, "payment/initiate_payment.html", context)


@csrf_exempt
def process_payment(request):
	if request.method == "POST":
		# Log raw data for debugging
		print("Raw Data:", request.POST)

		# Convert the QueryDict to a regular dictionary
		post_data = request.POST.dict()

		# Extract fields from the POST data
		rs = request.POST.get("RS")

		id = request.POST.get("ID")
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

		# Validate hash
		expected_hash = hashlib.sha512(
			f"{id}|{response_code}|{ref_no}|{service_tax_amount}|{processing_fee}|{total_amount}|{transaction_amount}|{transaction_date}|{intercharge_value}|{tdr}|{payment_mode}|{submerchant_id}|{ref_no_2}|{tps}|{AES_KEY}".encode()
		).hexdigest()

		# Prepare the response data (sending POST data as JSON response)
		response_data = {
			"received_data"     : post_data,
			"Reference No"      : ref_no,
			"Transaction Status": response_code,
			"Received RS"       : rs,
			"Expected RS"       : expected_hash,
			"Validation Result" : "Success" if rs == expected_hash else "Failed"
		}

		# Return JSON response with the POST data and validation result
		return JsonResponse(response_data)

	return JsonResponse({"error": "Invalid request method"}, status=405)
