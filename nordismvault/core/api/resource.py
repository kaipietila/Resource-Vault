from rest_framework import ApiView
from rest_framework import SessionAuthentication, BasicAuthentication
from rest_framework import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework import Response
from rest_framework import FileUploadParser

from core.models.contributor import Contributor
from core.models.resource import Resource
from core.utils import create_resource_and_tags
from core.utils import create_image_and_upload_to_drive


class ResourceSerializer(Serializer):
    code = Serializer.UUIDField()
    create_time = Serializer.DateTimeField()
    description = Serializer.TextField()
    tags = Serializer.PrimaryKeyRelatedField(many=True)
    contributor = Serializer.PrimaryKeyRelatedField()
    image = Serializer.PrimaryKeyRelatedField()

    class Meta:
        read_only_fields = ['code', 'create_time']


class ResourceApi(ApiView):
    http_method_names = ['get',]

    def get(self, request):
        contributor = Contributor.objects.get(user=request.user)
        contributed_resources = Resource.objects.get(contributor=contributor)
        return Response(data=ResourceSerializer(contributed_resources, many=True))


class UploadResource(ApiView):
    parser_classes = [FileUploadParser]

    def post(self, request, filename):
        uploaded_file = request.data['file']
        contributor_id = request.data['contributor_id']
        try:
            contributor = Contributor.objects.get(id=contributor_id)
            image = create_image_and_upload_to_drive(uploaded_file, contributor.user)
            create_resource_and_tags(request.data, image, contributor.user)
            return redirect('home')
        except ValidationError as e:
            render(request, 'add_resource.html', {'non_field_errors': e.message})
