from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import *


# Create your views here.
class GetVehicles(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.all()

        vehicle_serializer = VehicleSerializer(vehicles, many=True)

        return Response(vehicle_serializer.data)


class GetMaintenanceList(APIView):
    def get(self, request):
        maintenance_list = Maintenance.objects.all()

        maintenance_serializer = MaintenanceSerializer(maintenance_list, many=True)

        return Response(maintenance_serializer.data)
