from django.db import models

class ItemManager(models.Manager):
    def create_item(self, name, photo, price, description, type_item, **extra_fileds):
        item = self.model(name=name, price=price, description=description, type_item=type_item)
        item.save(using=self._db)
        return item