from functools import wraps
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
# from .models import ErrorLogger
from error_logging.logger import ErrorLogger

def catch_api_errors(app_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                return func(self, request, *args, **kwargs)
            except ObjectDoesNotExist as e:
                ErrorLogger.log(e, app=app_name, user=request.user if request.user.is_authenticated else None)
                return Response({"error": "Not found"}, status=404)
            except Exception as e:
                ErrorLogger.log(e, app=app_name, user=request.user if request.user.is_authenticated else None)
                return Response({"error": "An unexpected error occurred"}, status=500)
        return wrapper
    return decorator

def catch_admin_errors(app_name):
    def decorator(func):
        @wraps(func)
        def wrapper(modeladmin, request, *args, **kwargs):
            try:
                return func(modeladmin, request, *args, **kwargs)
            except Exception as e:
                user = request.user if request.user.is_authenticated else None
                ErrorLogger.log(e, app=app_name, user=user)
                raise
        return wrapper
    return decorator

def catch_errors(app_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ErrorLogger.log(e, app=app_name, user=None)
                raise
        return wrapper
    return decorator
