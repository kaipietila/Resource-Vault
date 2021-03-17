from rest_framework import ApiView
from rest_framework import SessionAuthentication, BasicAuthentication
from rest_framework import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework import Response

from core.models.contributor import Contributor
from core.models.resource import Resource

class ResourceSerializer(Serializer):
    code = Serializer.UUIDField()
    create_time = Serializer.DateTimeField()
    description = Serializer.TextField()
    tags = Serializer.PrimaryKeyRelatedField(many=True)
    contributor = Serializer.PrimaryKeyRelatedField()
    image = Serializer.PrimaryKeyRelatedField()


class ResourceApi(ApiView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request):
        contributor = Contributor.objects.get(user=request.user)
        contributed_resources = Resource.objects.get(contributor=contributor)
        return Response(data=ResourceSerializer(contributed_resources, many=True))
        