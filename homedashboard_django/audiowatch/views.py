from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from error_logging.logger import ErrorLogger
from classutils.discord_bot import send_discord_dm
import environ
import json

from .models import MicMonitorConfig, MicEventLog
from apps.models import ManagedDevice
from account.models import User

env = environ.Env()

@require_GET
def get_thresholds(request, machine_id):
    try:
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
    except Exception as e:
        ErrorLogger.log(e, app="audiowatch", user=None)
        # ErrorLogger().log_error(user=None, app="audiowatch", funct="get_thresholds", file="views.py", error=str(e), stack_trace=traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_POST
def submit_event(request):
    try:
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

    except Exception as e:
        ErrorLogger.log(e, app="audiowatch", user=None)
        return JsonResponse({"error": str(e)}, status=500)

def trigger_discord_alert(device, volume, event_type):
    try:
        print(device.fk_user_id)
        user = User.objects.get(id=device.fk_user_id.id)
        print(user)
        send_discord_dm(
            bot_token=env('AUDIOWATCH_API_TOKEN'),
            user_id=user.discord_user_id,
            message=f" Warning: Your mic volume hit {volume:.2f} dB. Please quiet down."
        )
    except Exception as e:
        ErrorLogger.log(e, app="audiowatch", user=None)


def trigger_vlan_block(machine_id):
    # Add VLAN cutoff logic here (e.g., SSH to switch)
    print(f"[VLAN] Cutting off access for: {machine_id}")
