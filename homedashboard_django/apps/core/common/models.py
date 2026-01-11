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

class CategoryLabel(models.Model):
    class Meta:
        verbose_name = "Category Label"
        verbose_name_plural = "Category Labels"
        db_table = 'category_labels'

    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name
    


class Category(CommonModel):
    class Meta(CommonModel.Meta):
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = 'category'
    label = models.ForeignKey(CategoryLabel, on_delete=models.CASCADE, blank=True, null=True)
    is_maint = models.BooleanField(default=False)
    is_catalog = models.BooleanField(default=False)
    is_tax_personal = models.BooleanField(default=False)
    is_tax_business = models.BooleanField(default=False)

class SubCategory(CommonModel):
    class Meta(CommonModel.Meta):
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"
        db_table = 'subcategory'

    name = models.CharField(max_length=200)
    
class Console(CommonModel):
    class Meta(CommonModel.Meta):
        verbose_name = "Console"
        verbose_name_plural = "Consoles"
        db_table = 'Console'

    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

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
        fname = getattr(self.file, "name", "<no file>")
        # Don't force resolution unless it's safe
        ct = self.content_type
        model_cls = ct.model_class() if ct else None

        if model_cls is None:
            return f"{fname} attached to <missing model {getattr(ct, 'app_label', '?')}.{getattr(ct, 'model', '?')}:{self.object_id}>"

        # Model exists; object might not
        obj = self.related_object
        if obj is None:
            return f"{fname} attached to <missing object {ct.app_label}.{ct.model}:{self.object_id}>"

        return f"{fname} attached to {obj}"