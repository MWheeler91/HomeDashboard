from django.contrib import admin
from .models import *
from classutils.admin import BaseModelAdmin
# from utils.admin import BaseModelAdmin
from classutils.common import catch_admin_errors
import re
# Register your models here.
from django.utils.html import format_html

              
class DefaultAdmin(BaseModelAdmin):              
    pass
# admin.site.register(Mileage)
# admin.site.register(AssetType)
# admin.site.register(Accessory)
# admin.site.register(VehicleRegistration, DefaultAdmin)


# shared inline classes
class MileageInline(admin.TabularInline):
    model = Mileage
    extra = 0
    can_delete = True
    fields = ("mileage", "date_entered")
    readonly_fields = ("date_entered","mileage")
    verbose_name_plural = "Mileage Log"
    verbose_name = "Mileage Entry"

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    can_delete = True
    fields = ("name", "is_active")
    show_change_link = True 
    verbose_name_plural = "Accessories"
    verbose_name = "Accessory"

class AccessoryInline(admin.TabularInline):
    model = Accessory
    # extra = 1
    can_delete = True
    fk_name = "fk_asset"
    fields = ("fk_asset", "brand", "short_description", "description", "purchased_from", "install_date", "purchase_date", "is_active")
    show_change_link = True 

class MaintenanceTaskInline(admin.TabularInline):
    model = MaintenanceTask
    extra = 0
    fields = ("name", "fk_category", "interval_days", "interval_miles", "reminder")
    show_change_link = True
    verbose_name_plural = "Maintenance Plan"
    verbose_name = "Task"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "fk_category":
            # Parent is Asset, so get asset_id from the URL:
            m = re.search(r"/asset/(\d+)/change/?$", request.path)
            if m:
                asset_id = int(m.group(1))
                asset = Asset.objects.select_related("fk_asset_type").get(pk=asset_id)

                kwargs["queryset"] = Category.objects.filter(
                    fk_asset_type_id=asset.fk_asset_type_id,
                    is_active=True,
                )
            else:
                # Adding a brand new Asset (no id yet)
                kwargs["queryset"] = Category.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class MaintenanceInline(admin.TabularInline):
    model = Maintenance
    extra = 0
    fields = ("task", "date_performed", "short_description")
    ordering = ("-date_performed",)
    show_change_link = True
    verbose_name_plural = "Service History"
    verbose_name = "Service Record"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "task":
            # Attempt to get the parent Asset ID from the admin URL
            m = re.search(r"/asset/(\d+)/change/?$", request.path)
            if m:
                asset_id = int(m.group(1))
                kwargs["queryset"] = MaintenanceTask.objects.filter(asset_id=asset_id)
            else:
                # When adding a new Asset (no ID yet), show none (or all, your choice)
                kwargs["queryset"] = MaintenanceTask.objects.none()


        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class TaskConsumableInline(admin.TabularInline):
    model = TaskConsumable
    extra = 1
    autocomplete_fields = ("consumable",)

    fields = ("consumable", "quantity", "brand", "part_number","notes","link")
    readonly_fields = ("brand", "part_number", "notes", "link")
    verbose_name_plural = "Consumables"
    verbose_name = "Consumable"

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "consumable":
            task_id = request.resolver_match.kwargs.get("object_id")
            if task_id:
                task = MaintenanceTask.objects.select_related(
                    "asset__fk_asset_type", "fk_category__fk_asset_type"
                ).get(pk=task_id)

                # If task has a category, only show consumables in that category
                if task.fk_category_id:
                    kwargs["queryset"] = Consumable.objects.filter(
                        fk_category_id=task.fk_category_id,
                        fk_category__is_active=True,
                    )
                else:
                    # No category selected yet → show none (or show all for that asset type if you prefer)
                    kwargs["queryset"] = Consumable.objects.none()
            else:
                # add page (no task id yet)
                kwargs["queryset"] = Consumable.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AccessoryAdmin(admin.ModelAdmin):
    model = Accessory
    search_fields = ("fk_asset","is_active")
    list_display = ("fk_asset",)
    # fieldsets = (
    #     (
    #         "Details",
    #         {
    #             "fields": (
    #                 "name",
    #                 "is_active",
    #             )
    #         },
    #     ),
    # )


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    model = AssetType
    search_fields = ("name","is_active")
    list_display = ("name",)
    inlines = (CategoryInline,)
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "name",
                    "is_active",
                )
            },
        ),
    )

@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    search_fields = ("name","fk_category", "brand", "part_number","fk_asset")
    list_display = ("name","fk_category", "brand", "part_number")
    fieldsets = (
        (
            "Consumable Details",
            {
                "fields": (
                    "fk_category",
                    "name",
                    "brand",
                    "part_number",
                    "notes",
                    "link",
                )
            },
        ),
    )


@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    model = MaintenanceTask
    list_display = ("name", "asset", "fk_category", "interval_days", "interval_miles", "next_due_date", "due_now", "reminder", "is_active")
    list_filter = ("reminder", "asset__asset_type")
    search_fields = ("name", "asset__name")
    readonly_fields = ('entered_by', 'date_entered', 'last_updated','last_updated_by')
    autocomplete_fields = ("asset",)
    
    fieldsets = (
        (
            "Task Details Details",
            {
                "fields": (
                    "name",
                    "asset",
                    "fk_category",
                    "interval_days",
                    "interval_miles",
                    "next_due_date",
                    "notes",
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
    )




    search_fields = ("title", "location_name")
    ordering = ("-due_now", "asset__asset_type")

    inlines = (TaskConsumableInline,)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("name", "fk_asset_type", "manufacturer", "model_name", "model_identifier", "serial_num", "warranty_expires")
    list_filter = ("fk_asset_type",)
    readonly_fields = ('entered_by', 'date_entered', 'last_updated','last_updated_by')
    search_fields = ("name", "location")
    inlines = (MaintenanceInline, MaintenanceTaskInline, AccessoryInline,MileageInline)
    fieldsets = (
        (
            "Asset Details",
            {
                "fields": (
                    # "id",
                    "name",
                    "is_active",
                    "fk_asset_type",
                    "location",
                    "manufacturer",
                    "model_name",
                    "model_identifier",
                    "serial_num",
                    "purchase_date",
                    "installed_date",
                    "warranty_expires",
                    "manual_url",
                    "notes",
                    "starting_mileage",
                    "current_mileage",
                    
                    "entered_by",
                    "date_entered",
                    "last_updated",
                    "last_updated_by",
                )
            },
        ),
    )

    def get_inline_instances(self, request, obj=None):
        """
        Only show the Vehicle inlines for vehicle assets (and only when editing an existing object).
        """
        inlines = []
        for inline_class in self.inlines:
            if inline_class in (AccessoryInline,MileageInline):
                if obj and obj.asset_type == "vehicle":
                    inlines.append(inline_class(self.model, self.admin_site))
            else:
                inlines.append(inline_class(self.model, self.admin_site))
        return inlines

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    model = Maintenance
    list_display = ("__str__", "short_description", "cost", "mileage")
    list_filter = ("asset__asset_type",)
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