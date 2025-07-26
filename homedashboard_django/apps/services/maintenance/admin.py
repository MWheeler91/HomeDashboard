from django.contrib import admin
from .models import *
from classutils.admin import BaseModelAdmin
from classutils.common import catch_admin_errors
# Register your models here.


# default admin class to set read only fields and set auto update saved by
class DefaultAdmin(BaseModelAdmin):
    pass

class MaintenanceAdmin(BaseModelAdmin):
    @catch_admin_errors('Maintenance')
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-date_performed')  # Orders by most recent first





admin.site.register(Vehicle, DefaultAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Accessory, DefaultAdmin)
admin.site.register(VehicleRegistration, DefaultAdmin)

