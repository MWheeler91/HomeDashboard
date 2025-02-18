from django.contrib import admin
from .models import *
from django.core.exceptions import ValidationError
from django.contrib import messages
# Register your models here.


# default admin class to set read only fields and set auto update saved by
class DefaultAdmin(admin.ModelAdmin):
    readonly_fields = (
        'entered_by',
        'date_entered',
        'last_updated_date',
        'last_updated_time',
        'last_updated_by'
    )

    def save_model(self, request, obj, form, change):
        # If the object is being created (not changed), set both fields
        if not change:
            obj.entered_by = request.user
        # For every save (including updates), set the last_updated_by field
        obj.last_updated_by = request.user

        super().save_model(request, obj, form, change)



class MaintenanceAdmin(admin.ModelAdmin):
    readonly_fields = (
        'entered_by',
        'date_entered',
        'last_updated_date',
        'last_updated_time',
        'last_updated_by'
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-date_performed')  # Orders by most recent first

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new, set entered_by
            obj.entered_by = request.user
        obj.last_updated_by = request.user  # Update last_updated_by for every save
        
        last_record = Maintenance.objects.filter(vehicle=obj.vehicle).order_by('-date_performed').first()
        if last_record and obj.mileage < last_record.mileage:
            messages.error(request, f"Mileage cannot be less than the previous record's mileage of {last_record.mileage}.")
            raise ValidationError("Mileage cannot be less than the previous record's mileage.")  # This prevents saving
            #return  # Prevent further processing and saving

        super().save_model(request, obj, form, change)



admin.site.register(Category)
admin.site.register(Vehicle, DefaultAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(MaintenanceFile)
admin.site.register(Accessory, DefaultAdmin)
admin.site.register(AccessoriesFile)
admin.site.register(VehicleRegistration, DefaultAdmin)

