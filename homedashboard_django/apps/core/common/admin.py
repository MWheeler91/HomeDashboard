from django.contrib import admin
from .models import *
from classutils.admin import BaseModelAdmin


# Register your models here.
class DefaultAdmin(BaseModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', "label",'is_maint', 'is_catalog', 'is_tax_business', 'is_tax_personal')
    list_filter = ('is_maint', 'is_catalog','is_tax_business', 'is_tax_personal')


admin.site.register(CategoryLabel)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Room)
admin.site.register(Condition)
admin.site.register(Console)
admin.site.register(File, DefaultAdmin)