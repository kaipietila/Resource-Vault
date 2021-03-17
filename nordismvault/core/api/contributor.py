from rest_framework import ApiView
from rest_framework import SessionAuthentication, BasicAuthentication
from rest_framework import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer
from rest_framework import Response
from rest_framework import ValidationError
from django.contrib.auth.models import User

from core.models.contributor import Contributor
from core.views.user_management import create_contributor


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', ]


class ContributorSerializer(Serializer):
    user = UserSerializer()
    verified = Serializer.BooleanField()
    
    class Meta:
        read_only_fields = ['verified']
        

class ContributorApi(ApiView):
    http_method_names = ['post', 'get']

    def post(self, request):
        serializer = UserSerializer(request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            create_contributor(user)
            return Response(status_code=201)
        except ValidationError as e:
            return Response(data=e.detail, status_code=400)

    def get(self, request):
        user_id = request.data['user_id']
        if user_id:
            user = User.objects.get(id=user_id)
            return Response(data=ContributorSerializer(user.contributor))
        else:
            return Response(data='Invalid payload', status_code=400)
