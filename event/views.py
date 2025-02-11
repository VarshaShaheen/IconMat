from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Participant, CheckIn

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_in(request):
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data')
        iconmat_id = request.POST.get('iconmat_id')

        if qr_code_data:
            for line in qr_code_data.strip().split("\n"):
                if line.startswith("iconmat ID:"):
                    iconmat_id = line.split(":")[1].strip()
                    break

        if not iconmat_id:
            return JsonResponse({"status": "error", "message": "No iconmat_id provided"}, status=400)

        try:
            participant = Participant.objects.get(iconmat_id=iconmat_id)

            # Check if participant already checked in
            if CheckIn.objects.filter(participant=participant).exists():
                return JsonResponse({"status": "info", "message": f"{participant.name} has already checked in."}, status=200)

            # Create new check-in record
            check_in_entry = CheckIn(participant=participant)
            check_in_entry.save()

            return JsonResponse({"status": "success", "message": f"Check-in successful for {participant.name}."}, status=200)

        except Participant.DoesNotExist:
            return JsonResponse({"status": "error", "message": f"No participant found for ID {iconmat_id}"}, status=404)

    return render(request, 'event/scan_qr.html')