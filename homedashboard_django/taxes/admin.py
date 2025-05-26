from django.contrib import admin
from .models import *
from classutils.admin import BaseModelAdmin
# Register your models here.


class DefaultAdmin(BaseModelAdmin):
    pass


admin.site.register(TaxYear, DefaultAdmin)
admin.site.register(Business, DefaultAdmin)
admin.site.register(WriteOffCategory)
admin.site.register(WriteOff, DefaultAdmin)

