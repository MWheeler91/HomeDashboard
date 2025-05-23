from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Prefetch
from .serializers import *
from classutils.common import catch_api_errors
# Create your views here.


class GetValues(APIView):
    @catch_api_errors('catalog')
    def get(self, request):
        rooms = Room.objects.all()
        condition = Condition.objects.all()
        category = Category.objects.all()

        room_serializer = RoomSerializer(rooms, many=True)
        condition_serializer = ConditionSerializer(condition, many=True)
        category_serializer = CategorySerializer(category, many=True)
        
        room_list = [item["room"] for item in room_serializer.data]
        condition_list = [item["condition"] for item in condition_serializer.data]
        category_list = [item["item_category"] for item in category_serializer.data]

        data = {
            "room": room_list,
            "condition": condition_list,
            "category": category_list,
        }

        return Response(data)


class NewItem(APIView):
    @catch_api_errors('catalog')
    def post(self, request):
        room_id = Room.objects.get(room=request.data["room"])
        item_category_id = Category.objects.get(
            item_category=request.data["item_category"]
        )
        condition_id = Condition.objects.get(condition=request.data["condition"])

        request.data["room"] = room_id.id
        request.data["item_category"] = item_category_id.id
        request.data["condition"] = condition_id.id

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
    @catch_api_errors('catalog')
    def delete(self, request, id):
        item = Item.objects.get(pk=id)
        item.delete()

        return Response(
            {"message": "Item deleted successfully"}, status=status.HTTP_200_OK
        )



class UpdateItem(APIView):
    @catch_api_errors('catalog')
    def put(self, request, id):
        room_id = Room.objects.get(room=request.data["room"])
        item_category_id = Category.objects.get(
            item_category=request.data["item_category"]
        )
        condition_id = Condition.objects.get(condition=request.data["condition"])

        item = Item.objects.get(id=request.data["id"])
        item.item_name = request.data["item_name"]
        item.item_description = request.data["item_description"]
        item.item_category = item_category_id
        item.condition = condition_id
        item.room = room_id
        item.serial_number = request.data['serial_number']
        item.model_number = request.data['model_number']
        item.value = request.data["value"]
        item.save()
        return Response(
            {"message": "Item updated successfully"}, status=status.HTTP_200_OK
        )



class GetAllItems(APIView):
    catch_api_errors('catalog')
    def get(self, request):
        # To reduce the number of database queries to get the string values this will call the setup_eager_loading function
        # in the serializer to pre petch all the related names.
        # https://docs.djangoproject.com/en/5.0/ref/models/querysets/#prefetch-related
        items = GetAllItemSerializer.setup_eager_loading(Item.objects.all().prefetch_related(
            Prefetch('item_category', queryset=Category.objects.all()),
            Prefetch('condition', queryset=Condition.objects.all()),
            Prefetch('room', queryset=Room.objects.all()),
            Prefetch('entered_by', queryset=User.objects.all()),
            ))
        serializer = GetAllItemSerializer(items, many=True)
        return Response(serializer.data)

