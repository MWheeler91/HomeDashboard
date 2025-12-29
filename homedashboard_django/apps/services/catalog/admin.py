from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from classutils.admin import BaseModelAdmin
from .models import *

# Register your models here.
# admin.site.register(Room)
# admin.site.register(Category)
# admin.site.register(Condition)

class ItemAccessoriesAdmin(BaseModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

class ItemAdmin(BaseModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(NatashaCollection)
class NatashaCollectionAdmin(admin.ModelAdmin):
    list_display = ['item_name','item_description','fk_category','cib','sealed','selling']
    list_filter = ["fk_category"]
    search_fields = ["item_name"]

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemAccessories, ItemAccessoriesAdmin)


# admin.site.register(NatashaCollection)
