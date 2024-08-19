from django.contrib import admin
from .models import App, ServerStatus
# Register your models here.
admin.site.register(App)
admin.site.register(ServerStatus)