from django.urls import path
from catalog import views

app_name = "catelog"

urlpatterns = [
    path('get-vehicles', views.GetValues.as_view(), name='getvalues'),
    path('new-maintenance', views.NewItem.as_view(), name='newitem' ),
    path('maintenance-list', views.GetAllItems.as_view(), name='itemlist' ),
    path('delete-maintenance/<int:id>', views.DeleteItem.as_view(), name='deleteitem' ),
    path('update-maintenance/<int:id>', views.UpdateItem.as_view(), name='updateitem' ),
]