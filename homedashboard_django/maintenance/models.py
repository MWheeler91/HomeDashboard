import os
from django.db import models
from datetime import datetime

# Create your models here.
from account.models import User


# ------------------  Custom Functions -------------------
def maintenance_file_upload_path(instance, filename):
    vehicle_folder = f"uploads/maintenance_files/{instance.maintenance.vehicle}/"
    return os.path.join(vehicle_folder, filename)


class Vehicle(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    trim = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    vin_number = models.CharField(max_length=17, default="")
    license_plate_number = models.CharField(max_length=10, blank=True, null=True)
    starting_mileage = models.IntegerField()
    is_active = models.BooleanField(default=True)    
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='vehicles')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    mileage = models.IntegerField()
    short_description = models.CharField(max_length=50)
    maintenance_performed = models.TextField()
    cost = models.DecimalField(max_digits=100, decimal_places=2)
    date_performed = models.DateField(default=datetime.now)
    next_service_date = models.DateField(blank=True, null=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='maintence')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_query_name='maintenance_updated')
    

    # part details ( part used / part number )

    def __str__(self):
        return f"{self.vehicle} - {self.short_description}"
    
    class Meta:
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenance"


class MaintenanceFile(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.SET_NULL, null=True)
    date_entered = models.DateField(default=datetime.now)
    updated_date = models.DateField(auto_now=True, blank=True, null=True)
    updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    files = models.FileField(
        upload_to=maintenance_file_upload_path, blank=True, null=True
    )

    def file_name(self):
        return os.path.basename(self.files.name)

    def __str__(self):
        return os.path.basename(self.files.name)


class Accessory(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
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
        return f"{self.vehicle} - {self.short_description}"
    
    class Meta:
        verbose_name = "Accessory"
        verbose_name_plural = "Accessories"


class AccessoriesFile(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    accessory = models.ForeignKey(Accessory, on_delete=models.SET_NULL, null=True)
    files = models.FileField(upload_to="uploads/accessories/", blank=True, null=True)
    date_entered = models.DateField(default=datetime.now)
    updated_date = models.DateField(auto_now=True, blank=True, null=True)
    updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def file_name(self):
        return os.path.basename(self.files.name)

    def __str__(self):
        return os.path.basename(self.files.name)
    

class VehicleRegistration(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
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



