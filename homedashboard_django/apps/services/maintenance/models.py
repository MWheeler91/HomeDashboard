import os
from django.db import models
from datetime import datetime, date,timedelta
# from apps.core.common.models import Category
from apps.core.account.models import User
from utils.models import BaseModel
from django.db.models import Max
from django.core.exceptions import ValidationError

# can't delete.  Django complains.  Fix at a later date.
def maintenance_file_upload_path(instance, filename):
    vehicle_folder = f"uploads/maintenance_files/{instance.maintenance.vehicle}/"
    return os.path.join(vehicle_folder, filename)

# TODO (Mileage edge case):
# If a Maintenance record's `asset` is ever changed after creation (Vehicle A → Vehicle B),
# the mileage for BOTH vehicles may need to be recomputed.
# Currently we only recompute the NEW vehicle, which could leave the OLD vehicle's
# current_mileage incorrect.
#
# When revisiting:
# - Decide whether Maintenance.asset should be immutable after creation
# - OR add logic to recompute mileage for the previous asset as well

class AssetType(models.Model):
    class Meta():
        ordering = ['name']
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta():
        ordering = ['name']
        unique_together = ("name", "fk_asset_type")
    fk_asset_type = models.ForeignKey(AssetType, on_delete=models.PROTECT, related_name='category', verbose_name='Asset Type', limit_choices_to={'is_active':True})
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.fk_asset_type})'


class Asset(BaseModel):
    ASSET_TYPES = (
        ("vehicle", "Vehicle"),
        ("home", "Home"),
        ("system", "System"),
        ("appliance", "Appliance")
    )
    name = models.CharField(max_length=100)
    fk_asset_type = models.ForeignKey(AssetType, on_delete=models.PROTECT, related_name='asset', verbose_name='Asset Type', limit_choices_to={'is_active':True}, blank=True, null=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    location = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    # shared
    manufacturer = models.CharField(max_length=100, blank=True, null=True) 
    model_name = models.CharField(max_length=100, blank=True,null=True)
    model_identifier = models.CharField(max_length=100, blank=True,null=True)
    serial_num = models.CharField(max_length=100, blank=True,null=True, verbose_name='Serial/VIN')
    purchase_date = models.DateField(blank=True, null=True)
    installed_date = models.DateField(blank=True, null=True)
    warranty_expires = models.DateField(blank=True, null=True)
    manual_url = models.URLField(blank=True, null=True)
    # vehicle-only (nullable)
    starting_mileage = models.IntegerField(blank=True, null=True)
    current_mileage = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    

    def recompute_current_mileage(self, save=True):
        if not self.asset_type == 'vehicle':
            return None

        max_mileage = (
            Mileage.objects
            .filter(fk_asset=self, mileage__isnull=False)
            .aggregate(Max("mileage"))["mileage__max"]
        )

        if max_mileage != self.current_mileage:
            self.current_mileage = max_mileage
            if save:
                self.save(update_fields=["current_mileage"])

        return max_mileage

class Consumable(BaseModel):
    class Meta(BaseModel.Meta):
        ordering = ["name"]
    
    fk_category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="consumables",
        limit_choices_to={"is_active": True},
        blank=True, null=True
    )
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True, null=True)
    part_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.CharField(max_length=255,blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Mileage(BaseModel):
    class Meta(BaseModel.Meta):
        indexes = [models.Index(fields=["fk_asset", "mileage"])]
        ordering =['-date_entered']

    fk_asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="mileage",
        limit_choices_to={"asset_type": "vehicle"},
        null=True,
        blank=True,
    )
    mileage=models.IntegerField()

    def __str__(self):
        return f'{self.mileage}'



class MaintenanceTask(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name="tasks")
    fk_category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="tasks",
        limit_choices_to={"is_active": True},
        verbose_name="Category",
    )
    name = models.CharField(max_length=100)
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    interval_days = models.PositiveIntegerField(null=True, blank=True)
    interval_miles = models.PositiveIntegerField(null=True, blank=True)
    reminder = models.BooleanField(default=True)
    due_now = models.BooleanField(default=True)
    next_due_date = models.DateField(blank=True,null=True)
    notes = models.TextField(blank=True, null=True)
    consumables = models.ManyToManyField(
        Consumable, through="TaskConsumable", blank=True, related_name="tasks"
    )

    def clean(self):
        super().clean()
        if self.asset_id and self.fk_category_id:
            if self.fk_category.fk_asset_type_id != self.asset.fk_asset_type_id:
                print(self.fk_category.fk_asset_type_id)
                print(self.asset.fk_asset_type_id)
                raise ValidationError({"fk_category": "Category must match this asset's type."})

    def __str__(self):
        return self.name

class TaskConsumable(models.Model):
    task = models.ForeignKey(MaintenanceTask, on_delete=models.PROTECT)
    consumable = models.ForeignKey(Consumable, on_delete=models.PROTECT)
    quantity = models.FloatField(default=1)

    def __str__(self):
        return self.task.name



class Maintenance(BaseModel):
    class Meta(BaseModel.Meta):
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenance"

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, null=True, blank=True)
    task = models.ForeignKey(MaintenanceTask, on_delete=models.PROTECT, null=True, blank=True)
    mileage = models.IntegerField(null=True, blank=True)
    short_description = models.CharField(max_length=50, default="", null=True, blank=True)
    maintenance_performed = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=100, decimal_places=2,null=True, blank=True)
    date_performed = models.DateField(default=datetime.now)

    def __str__(self):
        return f"{self.date_performed.strftime('%m/%d/%Y')} - {self.asset} - {self.task}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_mileage = None
        was_completed = False

        if not is_new:
            previous = Maintenance.objects.only("mileage", "completed").get(pk=self.pk)
            old_mileage = previous.mileage
            was_completed = previous.completed

        super().save(*args, **kwargs)

        # Task completion transition
        if not was_completed and self.completed and self.task:
            task = self.task
            task.due_now = False
            if task.interval_days:
                task.next_due_date = self.date_performed + timedelta(days=task.interval_days)
            task.save(update_fields=["due_now", "next_due_date"])

        # Mileage logging + recompute
        should_log_mileage = (
            self.asset_id
            and self.mileage is not None
            and self.asset.asset_type == "vehicle"
            and (is_new or self.mileage != old_mileage)
        )

        if should_log_mileage:
            Mileage.objects.create(fk_asset_id=self.asset_id, mileage=self.mileage)
            self.asset.recompute_current_mileage()
      

class Accessory(models.Model):
    fk_asset = models.ForeignKey(
        Asset,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        limit_choices_to={"asset_type": "vehicle"},
    )
    # fk_vehicle_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    short_description = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    purchased_from = models.CharField(max_length=50, blank=True, null=True)
    install_date = models.DateField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name = "Still Own?")
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='accessories')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.fk_asset} - {self.short_description}"
    
    class Meta:
        verbose_name = "Accessory"
        verbose_name_plural = "Accessories"

    
class VehicleRegistration(models.Model):
    fk_asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"asset_type": "vehicle"},
    )
    # fk_vehicle_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    registration_expiration_date = models.DateField(blank=True, null=True)
    date_paid = models.DateField(blank=True, null=True)
    active_year = models.BooleanField()
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registration')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_query_name='registration_updated')

    def __str__(self):
        return os.path.basename(f"{self.registration_expiration_date.year - 1} - {self.fk_asset}")   







# class Vehicle(BaseModel):
#     fk_asset = models.OneToOneField(
#         Asset,
#         on_delete=models.CASCADE,
#         related_name="vehicle",
#         limit_choices_to={"asset_type": "vehicle"},
#         null=True,
#         blank=True,
#     )
#     year = models.IntegerField()
#     make = models.CharField(max_length=30)
#     model = models.CharField(max_length=30)
#     trim = models.CharField(max_length=30, blank=True, null=True)
#     description = models.CharField(max_length=50, blank=True, null=True)
#     vin_number = models.CharField(max_length=17, default="")
#     license_plate_number = models.CharField(max_length=10, blank=True, null=True)
#     starting_mileage = models.IntegerField(blank=True,null=True)
#     current_mileage = models.IntegerField(blank=True,null=True)
#     mileage_this_year = models.IntegerField(blank=True,null=True)

#     def __str__(self):
#         return f"{self.year} {self.make} {self.model}"
    
#     def recompute_current_mileage(self, save=True):
#         if not self.fk_asset_id:
#             return None

#         max_mileage = (
#             Mileage.objects
#             .filter(fk_asset_id=self.fk_asset_id, mileage__isnull=False)
#             .aggregate(Max("mileage"))["mileage__max"]
#         )

#         if max_mileage != self.current_mileage:
#             self.current_mileage = max_mileage
#             if save:
#                 self.save(update_fields=["current_mileage"])

#         return max_mileage