from typing import List
from django.db import models
from django.db.models.signals import post_save


class CustomManager(models.Manager):
    # По умолчанию bulk_create не вызывает post_save сигнал для каждого из сохранных объектов
    def bulk_create(self, objs: List, **kwargs) -> List:
        s = super(CustomManager, self).bulk_create(objs, **kwargs)
        for i in objs:
            post_save.send(i.__class__, instance=i, created=True)

        return s


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    objects = CustomManager()
