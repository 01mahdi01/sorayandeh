from symtable import Class

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema
from .models import Campaign, Participants, CampaignCategory
from .services import create_campaign, contribute
from rest_framework.pagination import PageNumberPagination
from sorayandeh.users.documents import YourModelDocument
from elasticsearch_dsl import Q
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
        user_id = request.user.id
        try:
            campaign = create_campaign(user_id=user_id, **validated_data)
            return Response(self.OutputCreateCampaignSerializer(campaign).data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"error": f"Database Error {ex}"}, status=status.HTTP_400_BAD_REQUEST)


class ContributeCampaign(APIView):
    class InputContributeCampaignSerializer(serializers.Serializer):
        participation_type = serializers.CharField(max_length=10)
        campaign_id = serializers.IntegerField()

    class OutputContributeCampaignSerializer(serializers.ModelSerializer):
        class Meta:
            model = Participants
            fields = "__all__"

    def post(self, request):
        user_id = request.user.id
        # finance=Finance.objects.get.........///////////////////////////////\\\\\\\\\\\\\\\\\\\\\#$%!##@4
        serializer = self.InputContributeCampaignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        campaign_id = serializer.validated_data["campaign_id"]
        participation_type = serializer.validated_data["participation_type"]
        print("*" * 20, campaign_id, participation_type)
        try:
            contributed = contribute(user_id=user_id, campaign_id=campaign_id, participation_type=participation_type)
            return Response(self.OutputContributeCampaignSerializer(contributed).data)
        except Exception as ex:
            return Response(f"Database Error {ex}", status=status.HTTP_400_BAD_REQUEST)


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
        category = serializers.CharField(source="category.title", read_only=True)

        class Meta:
            model = Campaign
            fields = "__all__"

    def post(self, request):
        serializer = self.InputFilterByCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.validated_data["category_id"]
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
        category = serializers.CharField(source="category.title", read_only=True)
        school = serializers.CharField(source="school.school.name", read_only=True)

        class Meta:
            model = Campaign
            fields = "__all__"

    def post(self, request):
        # Validate input
        serializer = self.InputSearchBySchoolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        school_name = serializer.validated_data["name"]
        query = Q("wildcard", school_name=school_name)

        # Get the page number from query parameters, defaulting to 1 if not provided
        page = int(request.query_params.get("page", 1))
        page_size = 10
        from_value = (page - 1) * page_size  # Elasticsearch's 'from' is 0-based

        # Elasticsearch query with pagination and sorting by 'id'
        results = YourModelDocument.search().query(query).sort("id").extra(size=page_size, from_=from_value).execute()

        # Extract campaign IDs from Elasticsearch results
        campaigns_ids = [result.meta.id for result in results]

        # Query the campaigns using the extracted IDs and optimize with select_related to avoid N+1 issue
        campaigns = Campaign.objects.select_related("school").filter(id__in=campaigns_ids).order_by("id")

        # Serialize the data and return the response
        serializer = self.OutputSearchBySchoolSerializer(campaigns, many=True)
        return Response(serializer.data)


class SearchByAddress(APIView):
    pass


class GetSingleCampaign(APIView):
    class InputGetSingleCampaignSerializer(serializers.Serializer):
        campaign_id = serializers.IntegerField()

    class OutputGetSingleCampaignSerializer(serializers.ModelSerializer):
        category = serializers.CharField(source="category.title", read_only=True)
        school = serializers.CharField(source="school.school.name", read_only=True)

        class Meta:
            model = Campaign
            fields = "__all__"

    def post(self, request):
        serializer = self.InputGetSingleCampaignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        campaign_id = serializer.validated_data["campaign_id"]
        campaign = Campaign.objects.select_related("category", "school").get(pk=campaign_id)
        return Response(self.OutputGetSingleCampaignSerializer(campaign).data)


class GetCategories(APIView):
    class OutputGetCategoriesSerializer(serializers.ModelSerializer):
        class Meta:
            model = CampaignCategory
            fields = "__all__"

    def get(self, request):
        categories = CampaignCategory.objects.all()
        print(categories)
        return Response(self.OutputGetCategoriesSerializer(categories, many=True).data)
