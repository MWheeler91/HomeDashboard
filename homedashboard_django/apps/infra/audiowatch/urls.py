from django.urls import path
from . import views

app_name = 'audiowatch'

urlpatterns = [
    path('config/<str:machine_id>/', views.get_thresholds, name='get_thresholds'),
    path('event/', views.submit_event, name='submit_event'),
]
