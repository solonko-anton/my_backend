from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .manager import UserManager
# Create your models here.
class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email adress"))
    username = models.CharField(max_length=50, verbose_name=_("username"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now = True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    object = UserManager()

    def __str__(self):
        return self.email
    
    def tokens(self):
        pass


class OneTimePassword(models.Model):
    user=models.OneToOneField(Users, on_delete=models.CASCADE)
    code=models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user.username}-passcode"