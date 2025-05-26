from django.contrib import admin
from .models import *
from classutils.admin import BaseModelAdmin


# Register your models here.
class DefaultAdmin(BaseModelAdmin):
    pass



admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Condition)
admin.site.register(File, DefaultAdmin)