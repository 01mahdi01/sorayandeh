from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema
from .models import Campaign
from .services import create_campaign
from django.core.files.storage import default_storage
import os

class CreateCampaign(APIView):

    class InputCreateCampaignSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        campaign_category = serializers.IntegerField()
        applicant_info = serializers.JSONField()
        preview_images = serializers.ListField(child=serializers.ImageField(), required=True)
        estimated_money = serializers.IntegerField(required=True)

    class OutputCreateCampaignSerializer(serializers.ModelSerializer):
        class Meta:
            model = Campaign
            fields = "__all__"

    @extend_schema(responses=OutputCreateCampaignSerializer, request=InputCreateCampaignSerializer)
    def post(self, request):
        data = request.data

        serializer = self.InputCreateCampaignSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        user_id=request.user.id
        try:
            campaign = create_campaign(user_id=user_id, **validated_data)
            return Response(self.OutputCreateCampaignSerializer(campaign).data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(
                {"error": f"Database Error {ex}"},
                status=status.HTTP_400_BAD_REQUEST
            )
