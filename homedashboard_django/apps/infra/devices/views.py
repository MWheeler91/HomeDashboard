from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from classutils.common import catch_api_errors
from django.views.decorators.http import require_GET, require_POST
from .models import ManagedDevice
from django.shortcuts import get_object_or_404
# Create your views here.





@require_POST
@catch_api_errors('devices')
def check_device_details(request, host):
    device = get_object_or_404(
        ManagedDevice,
        hostname=host,
    )
    updated = False
    for field in ["os", "kernel_version", "cpu_cores", "ram_total_mb", "disk_total_gb", "agent_version"]:
        if field in request.data and getattr(device, field) != request.data[field]:
            setattr(device, field, request.data[field])
            updated = True

    if updated:
        device.save()
        return Response({"status": "updated"})
    return Response({"status": "no changes"})


    return JsonResponse({
    })
