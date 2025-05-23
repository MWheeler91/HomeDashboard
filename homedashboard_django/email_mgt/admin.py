from django.contrib import admin
from .models import *
from error_logging.logger import ErrorLogger
# Register your models here.


class DKIMAdmin(admin.ModelAdmin):
    readonly_fields = (
        'entered_by',
        'date_entered',
        'last_updated_date',
        'last_updated_time',
        'last_updated_by'
    )

    def save_model(self, request, obj, form, change):
        try:
            # If the object is being created (not changed), set both fields
            if not change:
                obj.entered_by = request.user
            # For every save (including updates), set the last_updated_by field
            obj.last_updated_by = request.user

            super().save_model(request, obj, form, change)
        except Exception as e:
            ErrorLogger.log(e, app="email_mgt", user=None)

class DKIM_RecordAdmin(admin.ModelAdmin):
    readonly_fields = (
        'entered_by',
        'date_entered',
        'last_updated_date',
        'last_updated_time',
        'last_updated_by'
    )

    def save_model(self, request, obj, form, change):
        try:
            # If the object is being created (not changed), set both fields
            if not change:
                obj.entered_by = request.user
            # For every save (including updates), set the last_updated_by field
            obj.last_updated_by = request.user

            super().save_model(request, obj, form, change)
        except Exception as e:
                    ErrorLogger.log(e, app="email_mgt", user=None)





admin.site.register(DKIM, DKIMAdmin)
admin.site.register(DKIM_Record, DKIM_RecordAdmin)