from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Maintenance)
admin.site.register(MaintenanceFile)
admin.site.register(Accessory)
admin.site.register(AccessoriesFile)