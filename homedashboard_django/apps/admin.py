from django.contrib import admin
from .models import App, ServerStatus,ManagedDevice,SshKeys
from classutils.admin import BaseModelAdmin
from classutils.common import catch_admin_errors

admin.site.register(App)
admin.site.register(ServerStatus)

class ManagedDeviceAdmin(BaseModelAdmin):
    catch_admin_errors("apps")
    def save_model(self, request, obj, form, change):
        if not obj.fk_user_id:
            obj.fk_user_id = request.user
        super().save_model(request, obj, form, change)

class SshKeysAdmin(BaseModelAdmin):
    pass

admin.site.register(ManagedDevice, ManagedDeviceAdmin)
admin.site.register(SshKeys, SshKeysAdmin)