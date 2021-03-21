from django.db import models
from uuid import uuid4

from core.models.contributor import Contributor


class Image(models.Model):
    drive_id = models.CharField(max_length=255)
    name = models.CharField(max_length=128)

    def __repr__(self):
        return self.name


class ResourceTag(models.Model):
    tag = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __repr__(self):
        return self.tag


class Resource(models.Model):
    code = models.UUIDField(default=uuid4)
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    contributor = models.ForeignKey(Contributor, on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(ResourceTag)

    def __repr__(self):
        return self.code
    
    def update_description(self, new_description):
        self.description = new_description
        self.save(update_fields=['description'])
    
    def add_tags(self, tags):
        for tag in tags:
            tag, _ = ResourceTag.objects.get_or_create(tag=tag)
            self.tags.add(tag.id)
