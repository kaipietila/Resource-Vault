from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response  import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import status

from core.views.user_management import create_contributor


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', ]


class ContributorSerializer(serializers.Serializer):
    user = UserSerializer()
    verified = serializers.BooleanField()
    
    class Meta:
        read_only_fields = ['verified']
        

class ContributorApi(APIView):
    http_method_names = ['post', 'get']

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            create_contributor(user)
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data=e.detail, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_id = request.data['user_id']
        if user_id:
            user = User.objects.get(id=user_id)
            return Response(data=ContributorSerializer(user.contributor), status=status.HTTP_200_OK)
        else:
            return Response(data='Invalid payload', status=status.HTTP_400_BAD_REQUEST)
