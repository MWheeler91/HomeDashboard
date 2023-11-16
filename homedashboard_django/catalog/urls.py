from django.urls import path
from catalog import views

app_name = "catalog"

urlpatterns = [
    path('get-values', views.GetValues.as_view(), name='getvalues'),
    path('new-item', views.NewItem.as_view(), name='newitem' ),
    path('item-list', views.GetAllItems.as_view(), name='itemlist' ),
    path('delete-item/<int:id>', views.DeleteItem.as_view(), name='deleteitem' ),
    path('update-item/<int:id>', views.UpdateItem.as_view(), name='updateitem' ),
]