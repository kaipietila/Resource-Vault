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


class ContributorSerializer(serializers.Serializer):
    user = UserSerializer()
    verified = serializers.BooleanField()
    
    class Meta:
        read_only_fields = ['verified']
        

class ContributorApi(APIView):
    http_method_names = ['get',]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            serializer = ContributorSerializer(user.contributor)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data='Invalid payload', status=status.HTTP_400_BAD_REQUEST)
