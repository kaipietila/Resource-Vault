from django.contrib.auth.models import User
from django.db import models

from uuid import uuid4


class Image(models.Model):
    drive_id = models.CharField(max_length=255)
    name = models.CharField(max_length=128)


class ResourceTag(models.Model):
    tag = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __repr__(self):
        return self.tag


class Resource(models.Model):
    code = models.UUIDField(default=uuid4)
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(ResourceTag)

    def __repr__(self):
        return self.code
