from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'item_category': "New Category"
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        labels = {
            'room': "Room"
        }


class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = '__all__'
        labels = {
            'condition': "Condition"
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        labels = {
            'item_name': 'Item',
            'item_description': 'Description',
            'item_category': 'Category',
            'condition': 'Condition',
            'room': 'Room',
            'value': 'Value',

        }
        exclude = {
            "date_entered"
        }