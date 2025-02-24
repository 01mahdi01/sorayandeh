from symtable import Class

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema
from .models import Campaign, Participants
from .services import create_campaign,contribute
from rest_framework.pagination import PageNumberPagination
from django.core.files.storage import default_storage
import os

class CreateCampaign(APIView):

    class InputCreateCampaignSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100)
        campaign_category = serializers.IntegerField()
        applicant_info = serializers.JSONField()
        preview_images = serializers.ListField(child=serializers.ImageField(), required=True)
        estimated_money = serializers.IntegerField(required=True)
        description = serializers.CharField(required=False)


    class OutputCreateCampaignSerializer(serializers.ModelSerializer):
        class Meta:
            model = Campaign
            fields = "__all__"

    @extend_schema(responses=OutputCreateCampaignSerializer, request=InputCreateCampaignSerializer)
    def post(self, request):
        data = request.data
        print(request.data)

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


class ContributeCampaign(APIView):
    class InputContributeCampaignSerializer(serializers.Serializer):
        participation_type = serializers.CharField(max_length=10)
        campaign_id=serializers.IntegerField()

    class OutputContributeCampaignSerializer(serializers.ModelSerializer):
        class Meta:
            model = Participants
            fields = "__all__"

    def post(self, request):
        user_id = request.user.id
        # finance=Finance.objects.get.........///////////////////////////////\\\\\\\\\\\\\\\\\\\\\#$%!##@4
        serializer = self.InputContributeCampaignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        campaign_id = serializer.validated_data['campaign_id']
        participation_type = serializer.validated_data['participation_type']
        print("*"*20,campaign_id,participation_type)
        try:
            contributed= contribute(user_id=user_id, campaign_id=campaign_id, participation_type = participation_type)
            return Response(self.OutputContributeCampaignSerializer(contributed).data)
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )


class CustomPagination(PageNumberPagination):
    page_size = 10  # Set the page size to 10


class CampaignList(APIView):
    class OutputCampaignListSerializer(serializers.ModelSerializer):
        category = serializers.CharField(source="category.title", read_only=True)

        class Meta:
            model = Campaign
            fields = "__all__"

    def get(self, request):
        # Optimize query by using select_related for category
        campaigns = Campaign.objects.select_related("category").all()

        # Initialize pagination
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(campaigns, request)

        # Serialize the paginated data
        serializer = self.OutputCampaignListSerializer(result_page, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)


class FilterByCategory(APIView):
    class InputFilterByCategorySerializer(serializers.Serializer):
        category_id = serializers.IntegerField()
    class OutputFilterByCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Campaign
            fields = "__all__"
    def get(self, request):
        serializer = self.InputFilterByCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.validated_data['category_id']
        campaigns = Campaign.objects.filter(category_id=category)
        # Initialize pagination
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(campaigns, request)

        # Serialize the paginated data
        serializer = self.OutputFilterByCategorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class SearchCampaignBySchool(APIView):
    class InputSearchBySchoolSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)  # School name

    class OutputSearchBySchoolSerializer(serializers.ModelSerializer):
        class Meta:
            model = Campaign
            fields = "__all__"

    def get(self, request):
        serializer = self.InputSearchBySchoolSerializer(data=request.query_params)  # Use query_params for GET requests
        serializer.is_valid(raise_exception=True)

        school_name = serializer.validated_data["name"]

        # Use select_related to optimize queries and avoid N+1 problem
        campaigns = Campaign.objects.select_related("school").filter(school__name__icontains=school_name)

        # Initialize pagination
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(campaigns, request)

        # Serialize the paginated data
        serializer = self.OutputSearchBySchoolSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



class GetSingleCampaign(APIView):
    pass

