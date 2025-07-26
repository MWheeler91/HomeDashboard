from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from classutils.models import CommonModel, BaseModel
# from maintenance.models import Vehicle
import os

def dynamic_upload_path(instance, filename):
    related_obj = instance.related_object
    if not related_obj:
        return f"uploads/unknown/{filename}"

    model_name = instance.content_type.model.lower()

    # Try to call a specific handler function
    handler_function = upload_path_handlers.get(model_name, default_upload_path)
    return handler_function(instance, filename)

def default_upload_path(instance, filename):
    model = instance.content_type.model
    return f"uploads/{model}/{filename}"

def get_upload_path_for_vehicle(instance, filename):
    vehicle = instance.related_object
    return f"uploads/vehicles/{vehicle.year}_{vehicle.make}_{vehicle.model}/{filename}"

def get_upload_path_for_accessory(instance, filename):
    accessory = instance.related_object
    vehicle = accessory.vehicle
    return f"uploads/vehicles/{vehicle.year}_{vehicle.make}_{vehicle.model}/accessories/{filename}"

def get_upload_path_for_taxyear(instance, filename):
    tax_year = instance.related_object  
    return f"uploads/taxes/{tax_year.year}/returns/{filename}"

def get_upload_path_for_writeoff(instance, filename):
    writeoff = instance.related_object 
    year = writeoff.tax_year.year
    business_name = writeoff.business.name if writeoff.business else "personal"
    category = writeoff.category.name if writeoff.category else "uncategorized"
    return f"uploads/taxes/{year}/{business_name}/{category}/{filename}"

upload_path_handlers = {
    'vehicle': get_upload_path_for_vehicle,
    'accessory': get_upload_path_for_accessory,
    'taxyear': get_upload_path_for_taxyear,
    'writeoff': get_upload_path_for_writeoff,
}


class Category(CommonModel):
    class Meta(CommonModel.Meta):
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = 'category'
    is_maint = models.BooleanField(default=False)
    is_catalog = models.BooleanField(default=False)
    is_tax_personal = models.BooleanField(default=False)
    is_tax_business = models.BooleanField(default=False)

class Room(CommonModel):
    class Meta(CommonModel.Meta):
        db_table = 'room'

class Condition(CommonModel):
    class Meta(CommonModel.Meta):
        db_table = 'condition'

class File(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = 'file'
    
    file = models.FileField(upload_to=dynamic_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Generic foreign key fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.file.name} attached to {self.related_object}"