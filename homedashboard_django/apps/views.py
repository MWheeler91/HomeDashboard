from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import AppSerializer
from .models import App
# Create your views here.


class AppList(APIView):
    def get(self, request):
        apps = App.objects.filter(is_active=True).order_by('app_name')
        serializer = AppSerializer(apps, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppListNoAuth(APIView):
    def get(self, request):
        apps = App.objects.filter(is_active=True, login_required=False).order_by('app_name')
        # filtered_apps = apps.objects.filter(login_required=False)
        serializer = AppSerializer(apps, many=True, context={'request':request})
        return Response(serializer.data)