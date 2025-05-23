from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from classutils.admin import BaseModelAdmin
from .models import *

# Register your models here.
admin.site.register(Room)
admin.site.register(Category)
admin.site.register(Condition)

class ItemAccessoriesAdmin(BaseModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

class ItemAdmin(BaseModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(Item, ItemAdmin)
admin.site.register(ItemAccessories, ItemAccessoriesAdmin)
