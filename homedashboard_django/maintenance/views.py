from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Prefetch
from .serializers import *
from .models import *


# Create your views here.
class GetVehicles(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.all()

        vehicle_serializer = VehicleSerializer(vehicles, many=True)

        # vehicle_list = [item["vehicle"] for item in vehicle_serializer.data]

        # data = {
        #     "vehicle": vehicle_list
        # }

        return Response(vehicle_serializer.data)

class GetValues(APIView):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        categories = Category.objects.all()

        vehicle_string_serializer = VehicleStringSerializer(vehicles, many=True)
        category_serializer = CategorySerializer(categories, many=True)

        vehicle_list = [item["vehicle_string"] for item in vehicle_string_serializer.data]
        category_list = [item["category"] for item in category_serializer.data]


        data = {
            "vehicle": vehicle_list,
            "category": category_list
        }
        print(data)
        return Response(data)

class GetMaintenanceList(APIView):
    def get(self, request):
        # To reduce the number of database queries to get the string values this will call the setup_eager_loading function
        # in the serializer to pre petch all the related names.
        # https://docs.djangoproject.com/en/5.0/ref/models/querysets/#prefetch-related
        maintenance_list = MaintenanceSerializer.setup_eager_loading(Maintenance.objects.all().prefetch_related(
            Prefetch('vehicle', queryset=Vehicle.objects.all()),
            Prefetch('category', queryset=Category.objects.all())
            ))
        serializer = MaintenanceSerializer(maintenance_list, many=True)
        return Response(serializer.data)


class DeleteMaintenance(APIView):
    def delete(self, request, id):
        try:
            # Get the item by ID
            maint_to_be_delete = Maintenance.objects.get(pk=id)
        except maint_to_be_delete.DoesNotExist:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Delete the item
        maint_to_be_delete.delete()

        return Response(
            {"message": "Item deleted successfully"}, status=status.HTTP_200_OK
        )
