from django.contrib import admin
from .models import *
from .forms import WriteOffForm
from classutils.admin import BaseModelAdmin
# Register your models here.


class DefaultAdmin(BaseModelAdmin):
    pass

class WriteOffAdmin(BaseModelAdmin):
    # form = WriteOffForm
    list_display = ('tax_year', 'fk_business', 'fk_category', 'description' ,'amount_payable', 'amount_receivable')
    list_filter = ('tax_year', 'fk_category', 'fk_business')

admin.site.register(TaxYear)
admin.site.register(Category)
admin.site.register(Business, DefaultAdmin)
admin.site.register(Ledger, WriteOffAdmin)

