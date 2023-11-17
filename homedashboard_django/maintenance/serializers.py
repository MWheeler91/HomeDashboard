# from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from .models import *


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "year",
            "make",
            "model",
            "trim",
            "year",
            "description",
            "starting_mileage",
            "date_entered",
            "entered_by",
            "is_active",
        ]


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = "__all__"


class MaintenanceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceFile
        fields = "__all__"


class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields =  "__all__"
        


class AccessoriesFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessoriesFile
        fields = "__all__"
        

    # def get_entered_by(self, obj):
    #     # Customize how you want to represent the 'entered_by' field
    #     return obj.entered_by.first_name
