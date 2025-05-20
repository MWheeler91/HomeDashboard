from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
import json

from .models import MicMonitorConfig, MicEventLog
from apps.models import ManagedDevice


@require_GET
def get_thresholds(request, machine_id):
    config = get_object_or_404(
        MicMonitorConfig,
        machine_id__hostname=machine_id,
        is_active=True
    )

    return JsonResponse({
        "machine_id": machine_id,
        "warning_threshold": config.warning_threshold,
        "cutoff_threshold": config.cutoff_threshold
    })


@csrf_exempt
@require_POST
def submit_event(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        machine_id = data.get("machine_id")
        volume = float(data.get("volume"))
        event_type = data.get("event_type")  # "warning" or "cutoff"

        if not machine_id or event_type not in ["warning", "cutoff"]:
            return JsonResponse({"error": "Invalid input"}, status=400)

        # Log event
        MicEventLog.objects.create(
            machine_id=machine_id,
            volume=volume,
            event_type=event_type
        )

        # Take action based on event type
        if event_type == "warning":
            trigger_discord_alert(machine_id, volume)
        elif event_type == "cutoff":
            trigger_vlan_block(machine_id)

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# === Stub Functions ===
def trigger_discord_alert(machine_id, volume):
    # Add Discord webhook logic here
    print(f"[DISCORD] {machine_id} yelled at {volume:.2f} dB")


def trigger_vlan_block(machine_id):
    # Add VLAN cutoff logic here (e.g., SSH to switch)
    print(f"[VLAN] Cutting off access for: {machine_id}")
