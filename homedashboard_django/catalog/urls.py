from django.contrib import admin
from django.urls import path, include
from catalog import views

app_name = "catalog"

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.mainview, name='main'),
    path('get-values', views.GetValues.as_view(), name='getvalues'),
    path('new-item', views.NewItem.as_view(), name='newitem' ),
    path('item-list', views.GetAllItems.as_view(), name='itemlist' ),
    path('delete-item/<int:id>', views.DeleteItem.as_view(), name='deleteitem' ),
    path('update-item/<int:id>', views.UpdateItem.as_view(), name='updateitem' ),



    path('new_item/', views.newview, name='new'),
    path('item_delete=<int:pk>/', views.ItemDeleteView.as_view(), name='delete' ),
    path('item_edit=<int:pk>/', views.ItemUpdateView.as_view(), name='edit' ),


    path('category_list/', views.CategoryListView.as_view(), name='category_list'),
    path('category_delete=<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete' ),
    path('category_edit=<int:pk>/', views.CategoryUpdateView.as_view(), name='category_edit' ),

    path('condition_list/', views.ConditionListView.as_view(), name='condition_list'),
    path('condition_delete=<int:pk>/', views.ConditionDeleteView.as_view(), name='condition_delete' ),
    path('condition_edit=<int:pk>/', views.ConditionUpdateView.as_view(), name='condition_edit' ),

    path('room_list/', views.RoomListView.as_view(), name='room_list'),
    path('room_delete=<int:pk>/', views.RoomDeleteView.as_view(), name='room_delete' ),
    path('room_edit=<int:pk>/', views.RoomUpdateView.as_view(), name='room_edit' ),




]