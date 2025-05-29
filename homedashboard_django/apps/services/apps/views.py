from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import AppSerializer
from .models import App
from classutils.common import catch_api_errors
# Create your views here.


class AppList(APIView):
    @catch_api_errors('apps')
    def get(self, request):
        apps = App.objects.filter(is_active=True).order_by('app_name')
        serializer = AppSerializer(apps, many=True, context={'request':request})
        return Response(serializer.data)

    @catch_api_errors('apps')
    def post(self, request):
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AppListNoAuth(APIView):
    @catch_api_errors('apps')
    def get(self, request):
        apps = App.objects.filter(is_active=True, login_required=False).order_by('app_name')
        # filtered_apps = apps.objects.filter(login_required=False)
        serializer = AppSerializer(apps, many=True, context={'request':request})
        return Response(serializer.data)