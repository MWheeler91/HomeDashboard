# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from rest_framework import status
# from rest_framework.generics import GenericAPIView


# from rest_framework.request import Request
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .serializers import UserCreateSerializer

from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    })
