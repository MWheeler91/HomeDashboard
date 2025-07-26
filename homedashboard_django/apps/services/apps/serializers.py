# from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from .models import *


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['app_name', 'web_address', 'icon', 'is_vue_app', 'login_required']








