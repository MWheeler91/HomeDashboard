from django.urls import path, include, reverse_lazy
from . import views

app_name = 'apps'

urlpatterns = [
    path('applist/', views.AppList.as_view()),
    path('applistnoauth/', views.AppListNoAuth.as_view()),
]