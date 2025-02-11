from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Participant, Lunch, Dinner

def process_check_in_by_iconmat_id(iconmat_id):
    """
    Common function to process check-in using the Iconmat ID.
    """
    try:
        participant = Participant.objects.get(iconmat_id=iconmat_id)
        if CheckIn.objects.filter(participant=participant).exists():
            return JsonResponse({
                "status": "info",
                "message": f"{participant.name} has already checked in."
            }, status=200)
        # Create a new check-in record
        CheckIn.objects.create(participant=participant)
        return JsonResponse({
            "status": "success",
            "message": f"Check-in successful for {participant.name}."
        }, status=200)
    except Participant.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": f"No participant found for ID {iconmat_id}."
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}."
        }, status=500)

@csrf_exempt
def process_qrcode(request):
    """
    Processes the QR code data, extracts the Iconmat ID, and checks in the participant.
    """
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data', '').strip()
        iconmat_id = ""
        if qr_code_data:
            # Extract iconmat_id from the QR code data
            for line in qr_code_data.split("\n"):
                if line.lower().startswith("iconmat id:"):
                    iconmat_id = line.split(":", 1)[1].strip()
                    break
        if not iconmat_id:
            return JsonResponse({
                "status": "error",
                "message": "No iconmat_id extracted from QR code."
            }, status=400)
        return process_check_in_by_iconmat_id(iconmat_id)
    return JsonResponse({
        "status": "error",
        "message": "Only POST requests allowed."
    }, status=405)

@csrf_exempt
def process_iconmat(request):
    """
    Processes manually submitted Iconmat ID for check-in.
    """
    if request.method == 'POST':
        iconmat_id = request.POST.get('iconmat_id', '').strip()
        if not iconmat_id:
            return JsonResponse({
                "status": "error",
                "message": "No iconmat_id provided."
            }, status=400)
        return process_check_in_by_iconmat_id(iconmat_id)
    return JsonResponse({
        "status": "error",
        "message": "Only POST requests allowed."
    }, status=405)

def scan_qr(request):
    """
    Renders the QR code scanning page.
    """
    return render(request, 'event/scan_qr.html')



def process_lunch_check_in(iconmat_id):
    try:
        participant = Participant.objects.get(iconmat_id=iconmat_id)
        today = timezone.localdate()
        if Lunch.objects.filter(participant=participant, timestamp__date=today).exists():
            return JsonResponse({
                "status": "info",
                "message": f"{participant.name} has already checked in for lunch today."
            }, status=200)
        Lunch.objects.create(participant=participant)
        return JsonResponse({
            "status": "success",
            "message": f"Lunch check-in successful for {participant.name}."
        }, status=200)
    except Participant.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": f"No participant found for ID {iconmat_id}."
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}."
        }, status=500)

def process_dinner_check_in(iconmat_id):
    try:
        participant = Participant.objects.get(iconmat_id=iconmat_id)
        today = timezone.localdate()
        if Dinner.objects.filter(participant=participant, timestamp__date=today).exists():
            return JsonResponse({
                "status": "info",
                "message": f"{participant.name} has already checked in for dinner today."
            }, status=200)
        Dinner.objects.create(participant=participant)
        return JsonResponse({
            "status": "success",
            "message": f"Dinner check-in successful for {participant.name}."
        }, status=200)
    except Participant.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": f"No participant found for ID {iconmat_id}."
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}."
        }, status=500)

# --- Processing Endpoints (QR-based) ---

@csrf_exempt
def lunch_qr_check_in(request):
    """
    Expects POST data with 'qr_code_data'. Extracts the Iconmat ID and processes the lunch check-in.
    """
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data', '').strip()
        iconmat_id = ""
        if qr_code_data:
            # Expecting a line like: "iconmat ID: XYZ123"
            for line in qr_code_data.split("\n"):
                if line.lower().startswith("iconmat id:"):
                    iconmat_id = line.split(":", 1)[1].strip()
                    break
        if not iconmat_id:
            return JsonResponse({
                "status": "error",
                "message": "No iconmat_id extracted from QR code."
            }, status=400)
        return process_lunch_check_in(iconmat_id)
    return JsonResponse({"status": "error", "message": "Only POST requests allowed."}, status=405)

@csrf_exempt
def dinner_qr_check_in(request):
    """
    Expects POST data with 'qr_code_data'. Extracts the Iconmat ID and processes the dinner check-in.
    """
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data', '').strip()
        iconmat_id = ""
        if qr_code_data:
            for line in qr_code_data.split("\n"):
                if line.lower().startswith("iconmat id:"):
                    iconmat_id = line.split(":", 1)[1].strip()
                    break
        if not iconmat_id:
            return JsonResponse({
                "status": "error",
                "message": "No iconmat_id extracted from QR code."
            }, status=400)
        return process_dinner_check_in(iconmat_id)
    return JsonResponse({"status": "error", "message": "Only POST requests allowed."}, status=405)

# --- Views for Rendering the Scanner Pages ---

def scan_lunch(request):
    """Renders the QR scanner page for lunch check-in."""
    return render(request, 'event/scan_lunch.html')

def scan_dinner(request):
    """Renders the QR scanner page for dinner check-in."""
    return render(request, 'event/scan_dinner.html')