from django.contrib.auth.models import User
from django.db import models

from uuid import uuid4


class Image(models.Model):
    file = models.ImageField(upload_to='images')
    code = models.CharField(max_length=255, blank=True)


class ResourceTag(models.Model):
    tag = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)


class Resource(models.Model):
    code = models.UUIDField(default=uuid4)
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(ResourceTag)
