from django.contrib import admin
from .models import App, ServerStatus,ManagedDevice,SshKeys
from classutils.admin import BaseModelAdmin


admin.site.register(App)
admin.site.register(ServerStatus)

class ManagedDeviceAdmin(BaseModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.user_fk:
            obj.user_fk = request.user
        super().save_model(request, obj, form, change)

class SshKeysAdmin(BaseModelAdmin):
    pass

admin.site.register(ManagedDevice, ManagedDeviceAdmin)
admin.site.register(SshKeys, SshKeysAdmin)