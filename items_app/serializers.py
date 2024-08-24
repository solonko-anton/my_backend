from .models import CreateItem
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class CreateItemSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = CreateItem
        fields = '__all__'


    def create(self, validated_data):
        items = CreateItem.object.create_item(
            name = validated_data.get('name'),
            price = validated_data.get('price'),
            description = validated_data.get('description'),
            type_item = validated_data.get('type_item'),
            photo=validated_data.get('photo')
        )
        return items
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.type_item = validated_data.get('type_item', instance.type_item)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance