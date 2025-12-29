from django.contrib import admin
from .models import *
from classutils.admin import BaseModelAdmin
# from utils.admin import BaseModelAdmin
from classutils.common import catch_admin_errors
# Register your models here.
from django.utils.html import format_html

# default admin class to set read only fields and set auto update saved by
class DefaultAdmin(BaseModelAdmin):
    pass

# class MaintenanceAdmin(BaseModelAdmin):
#     @catch_admin_errors('Maintenance')
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         return queryset.order_by('-date_performed')  # Orders by most recent first



# admin.site.register(Asset, DefaultAdmin)
# admin.site.register(Consumable, DefaultAdmin)
# admin.site.register(Vehicle, DefaultAdmin)
# admin.site.register(MaintenanceTask, DefaultAdmin)
# admin.site.register(TaskConsumable)
# admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Mileage)
admin.site.register(VehicleRegistration, DefaultAdmin)


@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    search_fields = ("name", "brand", "part_number")
    list_display = ("name", "brand", "part_number")
    fieldsets = (
        (
            "Consumable Details",
            {
                "fields": (
                    "name",
                    "brand",
                    "part_number",
                    "notes",
                    "link",
                )
            },
        ),
    )

class VehicleInline(admin.StackedInline):
    model = Vehicle
    extra = 0
    can_delete = False
    fk_name = "fk_asset"
    fields = ("year", "make", "model", "trim", "description", "vin_number", "license_plate_number", "starting_mileage","current_mileage","mileage_this_year")

class AccessoryInline(admin.TabularInline):
    model = Accessory
    extra = 1
    can_delete = True
    fields = ("short_description", "purchased_from", "purchase_date", "install_date", "brand")
    fk_name = "fk_asset"
    show_change_link = True 

class MaintenanceTaskInline(admin.TabularInline):
    model = MaintenanceTask
    extra = 0
    fields = ("name", "interval_days", "interval_miles", "reminder")
    show_change_link = True  # click into task to edit consumables

class MaintenanceInline(admin.TabularInline):
    model = Maintenance
    extra = 0
    fields = ("date_performed", "short_description", "cost", "mileage", "completed")
    ordering = ("-date_performed",)
    show_change_link = True


@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    model = MaintenanceTask
    list_display = ("name", "asset", "interval_days", "interval_miles", "next_due_date", "due_now", "reminder", "is_active")
    list_filter = ("reminder", "asset__asset_type")
    search_fields = ("name", "asset__name")
    readonly_fields = ('entered_by', 'date_entered', 'last_updated','last_updated_by')
    autocomplete_fields = ("asset",)
    fieldsets = (
        (
            "Task Details Details",
            {
                "fields": (
                    # "id",
                    "name",
                    "asset",
                    "interval_days",
                    "interval_miles",
                    "next_due_date",
                    "reminder",
                    "due_now",
                    "is_active",
                    "entered_by",
                    "date_entered",
                    "last_updated",
                    "last_updated_by",
                )
            },
        ),
        # (
        #     "Admin",
        #     {
        #         "fields": (
        #             "entered_by",
        #             "date_entered",
        #             "last_updated",
        #             "last_updated_by",
        #         )
        #     },
        # ),
    )




    search_fields = ("title", "location_name")
    ordering = ("-due_now", "asset__asset_type")


    class TaskConsumableInline(admin.TabularInline):
        model = TaskConsumable
        extra = 1
        autocomplete_fields = ("consumable",)

        fields = ("consumable", "quantity", "brand", "part_number","notes","link")
        readonly_fields = ("brand", "part_number", "notes", "link")

        @admin.display(description="Brand")
        def brand(self, obj):
            return obj.consumable.brand if obj.consumable_id else ""

        @admin.display(description="Part #")
        def part_number(self, obj):
            return obj.consumable.part_number if obj.consumable_id else ""

        @admin.display(description="Note #")
        def notes(self, obj):
            return obj.consumable.notes if obj.consumable_id else ""

        @admin.display(description="Order Link")
        def link(self, obj):
            if not obj.consumable_id or not obj.consumable.link:
                return ""
            return format_html('<a href="{}" target="_blank" rel="noopener">Open</a>', obj.consumable.link)


        


    inlines = (MaintenanceInline,TaskConsumableInline,)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("name", "asset_type", "location")
    list_filter = ("asset_type",)
    search_fields = ("name", "location")
    inlines = (VehicleInline, MaintenanceInline, MaintenanceTaskInline, AccessoryInline)

    def get_inline_instances(self, request, obj=None):
        """
        Only show the Vehicle inline for vehicle assets (and only when editing an existing object).
        """
        inlines = []
        for inline_class in self.inlines:
            if inline_class is VehicleInline or inline_class is AccessoryInline:
                if obj and obj.asset_type == "vehicle":
                    inlines.append(inline_class(self.model, self.admin_site))
            else:
                inlines.append(inline_class(self.model, self.admin_site))
        return inlines


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    model = Maintenance
    list_display = ("date_performed", "short_description", "cost", "mileage")
    list_filter = ("asset__asset_type", "fk_category_id")
    # search_fields = ("short_description", "asset__name")
    autocomplete_fields = ("asset", "task")
    readonly_fields = ('entered_by', 'date_entered', 'last_updated','last_updated_by')

    search_fields = ("asset", "task")
    
    autocomplete_fields = ("asset",)
    fieldsets = (
        (
            "Task Details Details",
            {
                "fields": (
                    # "id",
                    "asset",
                    "task",
                    "mileage",
                    "fk_category_id",
                    "short_description",
                    "maintenance_performed",
                    "completed",
                    "cost",
                    "date_performed",

                    "entered_by",
                    "date_entered",
                    "last_updated",
                    "last_updated_by",
                )
            },
        ),
    )