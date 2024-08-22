from rest_framework import serializers
from .models import Users
from .utils import send_normal_email
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_bytes, force_str
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


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


class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=6)
    password=serializers.CharField(max_length=68, write_only=True)
    full_name=serializers.CharField(max_length=255, read_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model=Users
        fields = '__all__'
    
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        request=self.context.get('request')
        user=authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("invalid credentials try again")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified") 
        user_tokens=user.tokens()
        return {
            'email':user.email,
            'username': user.username,
            'access_token':str(user_tokens.get('access_token')),
            'refresh_token':str(user_tokens.get('refresh_token'))
        }
    
class PasswordResetSerializer(serializers.Serializer):
    email=serializers.CharField(max_length=255)
    
    class Meta:
        fields=['email']

    def validate(self, attrs):
        email=attrs.get('email')
        if Users.object.filter(email=email).exists():
            user=Users.object.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            request=self.context.get('request')
            site_domain=get_current_site(request).domain
            relative_link=reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abslink=f"http://{site_domain}{relative_link}"
            email_body=f"reset password {abslink}"
            data={
                'email_body':email_body,
                'email_subject':"Reset your password",
                'to_email':user.email
            }
            send_normal_email(data)

        return super().validate(attrs)
    
class SetNewPasswordSerilizer(serializers.Serializer):
    new_password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    new_password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)

    class Meta:
        fields = '__all__'    
   
    def validate(self, attrs):
        try:
            new_password = attrs.get('new_password')
            new_password2 = attrs.get('new_password2')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("reset link is invalid or has expired", 401)
            if new_password != new_password2:
                raise AuthenticationFailed("passwords do not mutch")
            user.set_password(new_password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed("link is invlaid or has expired")
        
class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
        return super().save(**kwargs)