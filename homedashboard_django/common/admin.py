from django.contrib import admin
from .models import *
from classutils.admin import BaseModelAdmin


# Register your models here.
class DefaultAdmin(BaseModelAdmin):
    pass

<<<<<<< HEAD


admin.site.register(Category)
=======
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_maint', 'is_catalog', 'is_tax_business', 'is_tax_personal')
    list_filter = ('is_maint', 'is_catalog','is_tax_business', 'is_tax_personal')


admin.site.register(Category, CategoryAdmin)
>>>>>>> 319db39 (Fix: cleaned up accidental folder commit and committed correct changes)
admin.site.register(Room)
admin.site.register(Condition)
admin.site.register(File, DefaultAdmin)