# # from rest_framework import serializers
# # from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
# from rest_framework import serializers
# from .models import *


# class VehicleStringSerializer(serializers.ModelSerializer):
#     vehicle_string = serializers.SerializerMethodField()

#     class Meta:
#         model = Vehicle
#         fields = ['vehicle_string']
    
#     def get_vehicle_string(self, obj):
#         return str(obj)

# class VehicleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vehicle
#         fields = [
#             "id",
#             "year",
#             "make",
#             "model",
#             "trim",
#             "year",
#             "description",
#             "starting_mileage",
#             "date_entered",
#             "entered_by",
#             "is_active",
#             "__str__"
#         ]


# class MaintenanceSerializer(serializers.ModelSerializer):
#     vehicle = serializers.StringRelatedField()
#     category = serializers.StringRelatedField()

#     class Meta:
#         model = Maintenance
#         fields = [
#             "id",
#             "vehicle",
#             "category",
#             "short_description",
#             "maintenance_performed",
#             "mileage",
#             "cost",
#             "date_performed",
#             "next_service_date",

#         ]
#     def get_entered_by(self, obj):
#         return obj.entered_by.first_name

#     # Optimization the string related fields by prefetching the data.
#     @classmethod
#     def setup_eager_loading(cls, queryset):
#         queryset = queryset.select_related('vehicle', 'category')
#         # print(queryset)
#         return queryset

# class NewMaintenanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Maintenance
#         fields = [
#             "vehicle",
#             "category",
#             "short_description",
#             "maintenance_performed",
#             "cost",
#             "mileage",
#             "date_performed",
#             "next_service_date",
#             "entered_by"
            
#         ]

# class AccessorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Accessory
#         fields =  "__all__"
        
        

#     # def get_entered_by(self, obj):
#     #     # Customize how you want to represent the 'entered_by' field
#     #     return obj.entered_by.first_name
