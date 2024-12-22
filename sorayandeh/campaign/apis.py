from rest_framework import serializers
from rest_framework.views import APIView
from .models import Campaign, RequestCategory, Participants, Requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .services import create_campaign


class RequestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestCategory
        fields = '__all__'


class RequestsSerializer(serializers.ModelSerializer):
    category = RequestCategorySerializer(many=True)
    class Meta:
        model = Requests
        exclude = ['campaign']


class CreateCampaign(APIView):
    class CreateCampaignInputSerializer(serializers.Serializer):
        school_id = serializers.IntegerField()
        title = serializers.CharField(max_length=100)
        is_active = serializers.BooleanField(default=True)
        requests = RequestsSerializer(many=True)
        applicant_info = serializers.JSONField()
        preview_image = serializers.ImageField(required=False)
        video_link = serializers.URLField(required=False, allow_blank=True)
        estimated_money = serializers.IntegerField(default=0)

    class CreateCampaignOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Campaign
            fields = '__all__'


    def post(self, request,**kwargs):
        print(request.user.school_user.id)
        serializer = self.CreateCampaignInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fields = {key: value for key, value in serializer.validated_data.items() if value is not None}

        # campaign=create_campaign(**fields)

        print(request.data)






class Test(APIView):
    class InputSerializer(serializers.Serializer):
        category=RequestsSerializer()

    def get(self, request):
        serializer = self.InputSerializer()
        print(serializer)
        return Response(serializer.data)