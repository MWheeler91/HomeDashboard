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

# admin.site.register(TaxYear)
admin.site.register(Category)
admin.site.register(Business, DefaultAdmin)
admin.site.register(Ledger, WriteOffAdmin)


class LedgerInlines(admin.TabularInline):
    model = Ledger
    extra = 1
    can_delete = True
    show_change_link = True
    fields = ("fk_business", "fk_category","description","amount_payable","amount_receivable","date" )
    verbose_name = "Ledger"


@admin.register(TaxYear)
class TaxYearAdmin(admin.ModelAdmin):
    model=TaxYear
    search_fields = ("year","is_active",)
    list_display = ("year","notes", "is_active", "tax_return")
    
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "year",
                    "notes",
                    "tax_return",
                    "is_active"
                )
            },
        ),
    )

    inlines = (LedgerInlines,)
