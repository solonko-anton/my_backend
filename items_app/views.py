from .serializers import CreateItemSerializer 
from .models import CreateItem
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .permissions import IsOnwerOrReadOnly
class CreateItemView(APIView):

    serializer_class = CreateItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOnwerOrReadOnly]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(_('item created successfully'), status=status.HTTP_201_CREATED)
    
    def get(self, request, pk, format=None):
        item = [item.name for item in CreateItem.object.all()]
        description = [item.description for item in CreateItem.object.all()]
        type_item  = [item.type_item  for item in CreateItem.object.all()]
        price = [item.price  for item in CreateItem.object.all()]
        return Response({'name':item[pk], 'description':description[pk], 
                         'type_item':type_item[pk], 'price':price[pk]}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        instance = get_object_or_404(CreateItem, id=pk)
        serializer = CreateItemSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_("item updated successfully"), status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        item = CreateItem.object.get(id=pk)
        item.delete()
        return Response(_("item deleted successfully"), status=status.HTTP_204_NO_CONTENT)

    
    