from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from classutils.discord_bot import send_discord_dm
from datetime import date
from .models import MicMonitorConfig, MicEventLog
from apps.models import ManagedDevice
from account.models import User
from classutils.common import catch_api_errors
import environ, json

env = environ.Env()

@require_GET
# @catch_api_errors('audiowatch')
def get_thresholds(request, machine_id):
    print(f"Fetching config for machine_id: {machine_id}")
    config = get_object_or_404(
        MicMonitorConfig,
        fk_machine_id__hostname=machine_id,
        is_active=True
    )

    return JsonResponse({
        "machine_id": machine_id,
        "warning_threshold": config.warning_threshold,
        "cutoff_threshold": config.cutoff_threshold,
        "cooldown": config.cooldown
    })

@csrf_exempt
@require_POST
@catch_api_errors('audiowatch')
def submit_event(request):
    data = json.loads(request.body.decode('utf-8'))
    machine_id = data.get("machine_id")
    device = ManagedDevice.objects.get(hostname=machine_id)
    volume = data.get("volume")
    event_type = data.get("event_type")  # "warning" or "cutoff"

    print(device)
    if not machine_id or event_type not in ["warning", "cutoff"]:
        return JsonResponse({"error": "Invalid input"}, status=400)

    # Log event
    MicEventLog.objects.create(
        fk_machine_id=device,
        volume=volume,
        event_type=event_type
    )
    trigger_discord_alert(device, volume, event_type)

    return JsonResponse({"status": "ok"})


def trigger_discord_alert(device, volume, event_type):
    today = date.today()
    user = User.objects.get(id=device.fk_user_id.id)
    count = MicEventLog.objects.filter(
                fk_machine_id=device,
                event_type=event_type,
                timestamp__date=today
            ).count()
    
    send_discord_dm(
        bot_token=env('AUDIOWATCH_API_TOKEN'),
        user_id=user.discord_user_id,
        message=f" Warning: Your mic volume hit {volume:.2f} dB. Please quiet down.  You've had {count} {event_type.lower()} occurences today."
    )

    if user.id != 1:
        admin_user = User.objects.get(id=1)
        print(admin_user)
        send_discord_dm(
            bot_token=env('AUDIOWATCH_API_TOKEN'),
            user_id=admin_user.discord_user_id,
            message=f" {user.first_name} mic volume hit {volume:.2f} dB. This is their {count} {event_type.lower()} occurence today."
        )


def trigger_vlan_block(machine_id):
    # Add VLAN cutoff logic here (e.g., SSH to switch)
    print(f"[VLAN] Cutting off access for: {machine_id}")
