from django.db import models
from datetime import datetime
from account.models import User
# Create your models here.


class Category(models.Model):
    item_category = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return "{}".format(self.item_category)


class Room(models.Model):
    room = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return "{}".format(self.room)


class Condition(models.Model):
    condition = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return "{}".format(self.condition)

class ItemAccessories(models.Model):
    Item = models.ForeignKey(Item, limit_choices_to={'has_accessories':True}, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    value_now = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    model_number = models.CharField(max_length=50, blank=True, null=True)
    extra = models.JSONField(default=dict, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='items_Accessories')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_description = models.CharField(max_length=200, blank=True, null=True)
    item_category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    value_now = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    model_number = models.CharField(max_length=50, blank=True, null=True)
    asset_tag = models.CharField(max_length=50, blank=True, null=True)
    has_accessories = models.BooleanField(default=False)
    extra = models.JSONField(default=dict, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='items')
    date_entered = models.DateField(default=datetime.now)
    last_updated_date = models.DateField(auto_now=True, blank=True, null=True)
    last_updated_time = models.TimeField(auto_now=True,  blank=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        match self.item_category.item_category if self.item_category else None:
            case 'Server':
                return f"{self.id}: {self.item_name} - {self.asset_tag}"
            case _:
                return f"{self.id}: {self.item_name}"


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ItemAccessories.objects.filter(Item=self).update(is_active=self.is_active)