import hashlib

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


AES_KEY = "1400012609205020"  # Replace with your encryption key


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
			f"{id}|{response_code}|{ref_no}|{service_tax_amount}|{service_tax_amount}|{processing_fee}|{total_amount}|{transaction_amount}|{transaction_date}|{intercharge_value}|{tdr}|{payment_mode}|{submerchant_id}|{ref_no_2}|{tps}|{AES_KEY}".encode()
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


def initiate_payment(request):
	return render(request, "payment/initiate_payment.html")
