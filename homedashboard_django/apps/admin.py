from django.contrib import admin
from .models import App, ServerStatus,Server
# Register your models here.
admin.site.register(App)
admin.site.register(ServerStatus)
admin.site.register(Server)