import os
from django.db import models
from datetime import datetime
from classutils.models import BaseModel
from common.models import Category
# Create your models here.
from account.models import User


# can't delete.  Django complains.  Fix at a later date.
def maintenance_file_upload_path(instance, filename):
    vehicle_folder = f"uploads/maintenance_files/{instance.maintenance.vehicle}/"
    return os.path.join(vehicle_folder, filename)


class Vehicle(BaseModel):
    year = models.IntegerField()
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    trim = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    vin_number = models.CharField(max_length=17, default="")
    license_plate_number = models.CharField(max_length=10, blank=True, null=True)
    starting_mileage = models.IntegerField()
    is_active = models.BooleanField(default=True)    

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class Maintenance(models.Model):
    fk_vehicle_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    mileage = models.IntegerField()
    fk_category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, limit_choices_to={'app_laber': 'maintenance'}, null=True)
    short_description = models.CharField(max_length=50, default="")
    maintenance_performed = models.TextField()
    cost = models.DecimalField(max_digits=100, decimal_places=2)
    date_performed = models.DateField(default=datetime.now)
    next_service_date = models.DateField(blank=True, null=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='maintenance')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_query_name='maintenance_updated')
    

    # part details ( part used / part number )

    def __str__(self):
        return f"{self.date_performed.strftime('%m/%d/%Y')} - {self.fk_vehicle_id} - {self.fk_category_id} - {self.short_description}"
    
    class Meta:
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenance"
4

class Accessory(models.Model):
    fk_vehicle_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
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
        return f"{self.fk_vehicle_id} - {self.short_description}"
    
    class Meta:
        verbose_name = "Accessory"
        verbose_name_plural = "Accessories"

    
class VehicleRegistration(models.Model):
    fk_vehicle_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    registration_expiration_date = models.DateField(blank=True, null=True)
    date_paid = models.DateField(blank=True, null=True)
    active_year = models.BooleanField()
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registration')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_query_name='registration_updated')

    def __str__(self):
        return os.path.basename(f"{self.registration_expiration_date.year - 1} - {self.vehicle}")   



