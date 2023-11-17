from django.urls import path
from maintenance import views

app_name = "Maintenance"

urlpatterns = [
    path('get-vehicles', views.GetVehicles.as_view(), name='get-vehicles'),
    # path('new-maintenance', views.GetVehicles.as_view(), name='newitem' ),
    path('maintenance-list', views.GetMaintenanceList.as_view(), name='itemlist' ),
    # path('delete-maintenance/<int:id>', views.GetVehicles.as_view(), name='deleteitem' ),
    # path('update-maintenance/<int:id>', views.GetVehicles.as_view(), name='updateitem' ),
]