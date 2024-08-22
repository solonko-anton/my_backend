from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model=Users
        fields=['email', 'username', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("passwords do not mutch")
        return attrs

    def create(self, validated_data):
        user=Users.object.create_user(
            email=validated_data['email'],
            username=validated_data.get('username'),
            password=validated_data.get('password'),
        )


        return user

    
    
    