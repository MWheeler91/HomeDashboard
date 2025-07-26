from django.contrib import admin
from .models import App
from classutils.admin import BaseModelAdmin
from classutils.common import catch_admin_errors

admin.site.register(App)
# admin.site.register(ServerStatus)
