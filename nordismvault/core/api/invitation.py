from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.models.invitation import InvitationRequest
from core.utils import create_event_log

class InvitationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationRequest
        fields = ['email']

class InvitationRequestApi(APIView):

    def post(self, request):
        serializer = InvitationRequestSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            InvitationRequest.objects.create(
                email=serializer.validated_data['email']
            )
            create_event_log(action='invitation_api', payload=request.data, status=200)
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as e:
            create_event_log(action='invitation_api', payload=request.data, status=400, error_details=e.detail)
            return Response(status=status.HTTP_400_BAD_REQUEST)
