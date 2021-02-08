from django.core.files.storage import FileSystemStorage
from django.db import models

from uuid import uuid4

from core.models.contributor import Contributor

# local storage for testing
fs = FileSystemStorage(location='/resources')


class Resource(models.Model):
    code = models.UUIDField(default=uuid4)
    file = models.FileField(storage=fs)
    contributor = models.ForeignKey(Contributor, on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)


class ResourceTag(models.Model):
    tag = models.CharField(max_length=255)
    resource = models.ManyToManyField(Resource, related_name='tags')
    description = models.CharField(max_length=255, blank=True)
