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
		reference_no = request.POST.get("ReferenceNo")  # Use 'ReferenceNo' instead of 'Reference No' for consistency
		transaction_status = request.POST.get("Response Code")
		hash_val = request.POST.get("RS")

		# Validate hash
		expected_hash = hashlib.sha512(
			f"{reference_no}|{transaction_status}|{AES_KEY}".encode()
		).hexdigest()

		# Prepare the response data (sending POST data as JSON response)
		response_data = {
			"received_data"     : post_data,
			"Reference No"      : reference_no,
			"Transaction Status": transaction_status,
			"Received RS"       : hash_val,
			"Expected RS"       : expected_hash,
			"Validation Result" : "Success" if hash_val == expected_hash else "Failed"
		}

		# Return JSON response with the POST data and validation result
		return JsonResponse(response_data)

	return JsonResponse({"error": "Invalid request method"}, status=405)


def initiate_payment(request):
	return render(request, "payment/initiate_payment.html")
