# from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["item_category"]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["room"]


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ["condition"]


class NewItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "item_name",
            "item_description",
            "item_category",
            "condition",
            "room",
            "value",
            "serial_number",
            "model_number",
            "entered_by",
        ]


class GetAllItemSerializer(serializers.ModelSerializer):
    item_category = serializers.StringRelatedField()
    condition = serializers.StringRelatedField()
    room = serializers.StringRelatedField()
    entered_by = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "id",
            "item_name",
            "item_description",
            "item_category",
            "condition",
            "room",
            "value",
            "serial_number",
            "model_number",
            "date_entered",
            "entered_by",
        ]

    def get_entered_by(self, obj):
        return obj.entered_by.first_name

    # Optimization the string related fields by prefetching the data.
    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.select_related('item_category', 'condition', 'room', 'entered_by')
        return queryset