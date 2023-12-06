from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Room)
admin.site.register(Category)
admin.site.register(Condition)


class ItemAdmin(admin.ModelAdmin):
    readonly_fields = (
        'entered_by',
        'date_entered',
        'last_updated_date',
        'last_updated_time',
        'last_updated_by'
    )

    def save_model(self, request, obj, form, change):
        # If the object is being created (not changed), set both fields
        if not change:
            obj.entered_by = request.user
        # For every save (including updates), set the last_updated_by field
        obj.last_updated_by = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Item, ItemAdmin)
