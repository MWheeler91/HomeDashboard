from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from .models import *
from .forms import *
from .filters import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#everything above can be remoted
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response

from .serializers import *
from django.http import JsonResponse
from django.http import Http404





# Create your views here.

class GetValues(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        condition = Condition.objects.all()
        category = Category.objects.all()

        room_serializer = RoomSerializer(rooms, many=True)
        condition_serializer = ConditionSerializer(condition, many=True )
        category_serializer = CategorySerializer(category, many=True)

        room_list = [item["room"] for item in room_serializer.data]
        condition_list = [item["condition"] for item in condition_serializer.data]
        category_list = [item["item_category"] for item in category_serializer.data]

        data = {
            "room": room_list,  
            "condition": condition_list,
            "category": category_list
        }

        return Response(data)
    

class NewItem(APIView):
    def post(self, request):
        print(request.data)
        room_id = Room.objects.get(room=request.data['room'])
        item_category_id = Category.objects.get(item_category=request.data['item_category'])
        condition_id = Condition.objects.get(condition=request.data['condition'])

        request.data['room'] = room_id.id
        request.data['item_category'] = item_category_id.id
        request.data['condition'] = condition_id.id

        serializer = NewItemSerializer(data=request.data)

        if serializer.is_valid():
            print("serializer is good")
        else:
            print("it's bad")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteItem(APIView):
    def delete(self, request, id):
        print(request.data)
        print(request.data)
        try:
            # Get the item by ID
            item = Item.objects.get(pk=id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the item
        item.delete()

        return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)

class UpdateItem(APIView):
    def put(self, request, id):
        print(request.data)

        try:
            room_id = Room.objects.get(room=request.data['room'])
            item_category_id = Category.objects.get(item_category=request.data['item_category'])
            condition_id = Condition.objects.get(condition=request.data['condition'])

            item = Item.objects.get(id=request.data['id'])
            item.item_name = request.data['item_name']
            item.item_description = request.data['item_description']
            item.item_category = item_category_id
            item.condition = condition_id
            item.room = room_id
            item.value = request.data['value']
            item.save()
            return Response({"message": "Item updated successfully"}, status=status.HTTP_200_OK)

        except Item.DoesNotExist:
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND) 

        # serializer = NewItemSerializer(data=request.data)

        # if serializer.is_valid():
        #     print("serializer is good")
        # else:
        #     print("it's bad")
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetAllItems(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = GetAllItemSerializer(items, many=True)
        return Response(serializer.data)










# @api_view(['GET'])
def mainview(request):
    room_form = RoomForm(prefix='room')
    category_form = CategoryForm(prefix='category')
    condition_form = ConditionForm(prefix='condition')
    item_form = ItemForm(prefix='item')


    #shows item list
    item_list = Item.objects.all()
    item_filter = ItemFilter(request.GET, queryset=item_list)
    if item_filter.is_valid():
        item_list = item_filter.qs

    paginator = Paginator(item_list, 20)  # Show 20 items per page.
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'catalog/main.html', {'room': room_form,
                                                 'category': category_form,
                                                 'condition': condition_form,
                                                 'item': item_form,
                                                 'item_list': item_list,
                                                 'filter': item_filter,
                                                 'page_obj': page_obj,
                                                 })



def newview(request):
    room_form = RoomForm(request.POST, prefix='room')
    category_form = CategoryForm(request.POST, prefix='category')
    condition_form = ConditionForm(request.POST, prefix='condition')
    item_form = ItemForm(request.POST, prefix='item')
    if request.method == 'POST':
        if room_form.is_valid():
            room_form.save()
        if category_form.is_valid():
            category_form.save()
        if condition_form.is_valid():
            condition_form.save()
        if item_form.is_valid():
            item_form.save()
            print("this worked")
        return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'catalog/NewItem.html', {'room': room_form,
                                                        'category': category_form,
                                                        'condition': condition_form,
                                                        'item': item_form,
                                                        })


class HomeView(TemplateView):
    template_name = 'catalog/MAIN.html'



class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'catalog/itemedit.html'
    # redirect_field_name = ''
    form_class = ItemForm
    success_url = reverse_lazy("catalog:main")


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'catalog/deleteitem.html'
    success_url = reverse_lazy("catalog:main")


# -------------------- Category Views --------------------
class CategoryListView(ListView):
    model = Category

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'catalog/itemedit.html'
    # redirect_field_name = ''
    form_class = CategoryForm
    success_url = reverse_lazy("catalog:category_list")


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'catalog/deleteitem.html'
    success_url = reverse_lazy("catalog:category_list")


# -------------------- Condition Views --------------------
class ConditionListView(ListView):
    model = Condition


class ConditionUpdateView(UpdateView):
    model = Condition
    template_name = 'catalog/itemedit.html'
    form_class = ConditionForm
    success_url = reverse_lazy("catalog:condition_list")


class ConditionDeleteView(DeleteView):
    model = Condition
    template_name = 'catalog/deleteitem.html'
    success_url = reverse_lazy("catalog:condition_list")


# -------------------- Room Views --------------------
class RoomListView(ListView):
    model = Room


class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'catalog/itemedit.html'
    # redirect_field_name = ''
    form_class = RoomForm
    success_url = reverse_lazy("catalog:room_list")


class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'catalog/deleteitem.html'
    success_url = reverse_lazy("catalog:room_list")


