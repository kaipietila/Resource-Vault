from django.contrib import admin

from core.models.contributor import Contributor
from core.models.resource import Resource, ResourceTag, Image
from core.models.event_log import ApiEvent

admin.site.register(Resource)
admin.site.register(ResourceTag)
admin.site.register(Image)
admin.site.register(Contributor)

admin.site.register(ApiEvent)
