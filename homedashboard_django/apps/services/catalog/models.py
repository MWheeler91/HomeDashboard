from django.db import models
from datetime import datetime
from apps.core.account.models import User
from apps.core.common.models import Category, Room, Condition
# Create your models here

def get_json():
    return { 'Field1': [], 'Field2': [],'Field3': []}

# class Category_old(models.Model):
#     item_category = models.CharField(max_length=200, unique=True)

#     def __str__(self):
#         return "{}".format(self.item_category)

# class Room_old(models.Model):
#     room = models.CharField(max_length=200, unique=True)

#     def __str__(self):
#         return "{}".format(self.room)


# class Condition_old(models.Model):
#     condition = models.CharField(max_length=200, unique=True)

#     def __str__(self):
#         return "{}".format(self.condition)

class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_description = models.CharField(max_length=200, blank=True, null=True)
    fk_category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, limit_choices_to={'app_label': 'catalog'}, blank=True, null=True)
    fk_condition_id = models.ForeignKey(Condition, on_delete=models.SET_NULL, limit_choices_to={'app_label': 'catalog'}, blank=True, null=True)
    fk_room_id = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, limit_choices_to={'app_label': 'catalog'}, null=True)
    purchase_price = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    value_now = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    model_number = models.CharField(max_length=50, blank=True, null=True)
    asset_tag = models.CharField(max_length=50, blank=True, null=True)
    has_accessories = models.BooleanField(default=False)
    extra = models.JSONField(default=get_json, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='items')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        match self.fk_category_id.name if self.fk_category_id else None:
            case 'Server':
                return f"{self.id}: {self.item_name} - {self.asset_tag}"
            case _:
                return f"{self.id}: {self.item_name}"


    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if not is_new:
            # Get the previous state of the instance
            old_instance = type(self).objects.get(pk=self.pk)
            if old_instance.is_active != self.is_active and self.has_accessories:
                # Update related accessories only if is_active changed
                ItemAccessories.objects.filter(item=self).update(is_active=self.is_active)


        super().save(*args, **kwargs)  # Save after checking conditions
        

class ItemAccessories(models.Model):
    fk_item_id = models.ForeignKey(Item, limit_choices_to={'has_accessories':True}, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200)
    purchase_price = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    value_now = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    model_number = models.CharField(max_length=50, blank=True, null=True)
    extra = models.JSONField(default=get_json, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='items_Accessories')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}: {self.item.item_name} - {self.name}"