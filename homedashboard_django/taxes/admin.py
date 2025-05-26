from django.contrib import admin
from .models import *
from .forms import WriteOffForm
from classutils.admin import BaseModelAdmin
# Register your models here.


class DefaultAdmin(BaseModelAdmin):
    pass

class WriteOffAdmin(BaseModelAdmin):
    form = WriteOffForm
    list_display = ('tax_year', 'amount', 'category', 'business')
    list_filter = ('tax_year', 'category', 'business')

admin.site.register(TaxYear)
admin.site.register(Business, DefaultAdmin)
admin.site.register(WriteOff, WriteOffAdmin)

