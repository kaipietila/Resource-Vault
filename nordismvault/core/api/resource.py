from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status

from core.models.contributor import Contributor
from core.models.resource import Resource, ResourceTag, Image
from core.utils import create_resource
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

    def post(self, request):
        uploaded_file = request.data['file']
        if uploaded_file:
            image = create_image_and_upload_to_drive(uploaded_file, request.user)
            resource = create_resource(image, request.user)
            serializer = ResourceSerializer(resource)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data='Image missing', status=status.HTTP_400_BAD_REQUEST)
