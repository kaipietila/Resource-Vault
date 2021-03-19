from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response  import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import status

from core.views.user_management import create_contributor
from core.utils import create_event_log


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class ContributorSerializer(serializers.Serializer):
    user = UserSerializer()
    verified = serializers.BooleanField()
    
    class Meta:
        read_only_fields = ['verified']
        

class SignUpApi(APIView):
    http_method_names = ['post', 'get']

    def post(self, request):
        serializer = UserSerializer(data=request.data['data'])
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            create_contributor(user)
            create_event_log(payload=request.data, action='sign_up_api', user=user, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as e:
            create_event_log(payload=request.data, action='sign_up_api',
                            status=status.HTTP_400_BAD_REQUEST, error_details=e.detail)
            print(e.detail)
            return Response(data=e.detail, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_id = request.data['user_id']
        if user_id:
            user = User.objects.get(id=user_id)
            return Response(data=ContributorSerializer(user.contributor), status=status.HTTP_200_OK)
        else:
            return Response(data='Invalid payload', status=status.HTTP_400_BAD_REQUEST)
