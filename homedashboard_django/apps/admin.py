from django.contrib import admin
from .models import App, ServerStatus,ManagedDevice,SshKeys
# Register your models here.
admin.site.register(App)
admin.site.register(ServerStatus)
# admin.site.register(Server)


class ManagedDeviceAdmin(admin.ModelAdmin):

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

admin.site.register(ManagedDevice, ManagedDeviceAdmin)


class SshKeysAdmin(admin.ModelAdmin):

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

admin.site.register(SshKeys, SshKeysAdmin)