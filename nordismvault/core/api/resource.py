from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from core.models.contributor import Contributor
from core.models.resource import Resource, ResourceTag, Image
from core.utils import create_resource_and_tags
from core.utils import create_image_and_upload_to_drive


class ResourceSerializer(serializers.Serializer):
    code = serializers.UUIDField()
    create_time = serializers.DateTimeField()
    description = serializers.CharField()
    tags = serializers.PrimaryKeyRelatedField(queryset=ResourceTag.objects.all(), many=True)
    contributor = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all())
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())

    class Meta:
        read_only_fields = ['code', 'create_time']


class ResourceApi(ListAPIView):
    serializer_class = ResourceSerializer

    def get_queryset(self):
        user = self.request.user
        return Resource.objects.filter(contributor=user.contributor)


class UploadResource(APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, filename):
        uploaded_file = request.data['file']
        contributor_id = request.data['contributor_id']
        if uploaded_file:
            contributor = Contributor.objects.get(id=contributor_id)
            image = create_image_and_upload_to_drive(uploaded_file, contributor.user)
            resource = create_resource_and_tags(request.data, image, contributor.user)
            return Response(ResourceSerializer(resource), status_code=201)
        else:
            return Response(data='Image missing', status_code=400)
