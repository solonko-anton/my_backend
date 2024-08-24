from typing import Iterable
from django.db import models
from .manager import ItemManager
# Create your models here.

class CreateItem(models.Model):
    type_item = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=255)
    sale_date = models.DateField(auto_now_add=True)

    object = ItemManager()

    def __str__(self):
        return self.name

    