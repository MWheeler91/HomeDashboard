from django.contrib import admin
from classutils.admin import BaseModelAdmin
from classutils.common import catch_admin_errors
from .models import ManagedDevice,SshKeys,DeviceAuth
from .setup import setup_server

# Register your models here.
class ManagedDeviceAdmin(BaseModelAdmin):
    catch_admin_errors("devices")
    def save_model(self, request, obj, form, change):
        if not obj.fk_user_id:
            obj.fk_user_id = request.user


        if not obj.is_processed and not obj.is_active and obj.os == 'Linux':
            setup_server(obj)


        super().save_model(request, obj, form, change)

class BaseAdmin(BaseModelAdmin):
    pass

admin.site.register(ManagedDevice, ManagedDeviceAdmin)
admin.site.register(SshKeys, BaseAdmin)
admin.site.register(DeviceAuth, BaseAdmin)