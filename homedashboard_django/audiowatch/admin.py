from django.contrib import admin
from .models import MicMonitorConfig, MicEventLog
from classutils.admin import BaseModelAdmin

# Register your models here.
class MicMonitorConfigAdmin(admin.ModelAdmin):
    pass

class MicEventLogAdmin(BaseModelAdmin):
    readonly_fields = ('timestamp',) + BaseModelAdmin.readonly_fields

admin.site.register(MicMonitorConfig, MicMonitorConfigAdmin)
admin.site.register(MicEventLog, MicEventLogAdmin)