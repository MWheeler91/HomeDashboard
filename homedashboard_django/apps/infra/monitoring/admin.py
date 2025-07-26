from django.contrib import admin

# Register your models here.
from django.contrib import admin
from classutils.admin import BaseModelAdmin
from classutils.common import catch_admin_errors
from .models import MonitoringConfig,SystemSnapshot,SecurityAlert,ManualCheckLog

# Register your models here.
class BaseAdmin(BaseModelAdmin):
    pass

admin.site.register(MonitoringConfig, BaseAdmin)
admin.site.register(SystemSnapshot, BaseAdmin)
admin.site.register(SecurityAlert, BaseAdmin)
admin.site.register(ManualCheckLog, BaseAdmin)