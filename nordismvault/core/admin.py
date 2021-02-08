from django.contrib import admin

from core.models.contributor import Contributor
from core.models.resource import Resource, ResourceTag, Image

admin.site.register(Resource)
admin.site.register(ResourceTag)
admin.site.register(Contributor)
admin.site.register(Image)