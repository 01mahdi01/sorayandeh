from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import generate_payment_url
from ..campaign.models import Campaign
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404


from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)


class RequestPaymentUrl(APIView):
    class InputRequestPaymentSerializer(serializers.Serializer):
        amount = serializers.IntegerField()
        # campaign_id = serializers.IntegerField()
    class OutputRequestPaymentSerializer(serializers.Serializer):
        url = serializers.URLField()

    def post(self, request):
        serializer = self.InputRequestPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        # with transaction.atomic():
        #     campaign = Campaign.objects.select_for_update().get(pk=serializer.validated_data['campaign_id'])
        #     if amount > campaign.steel_needed_money:
        #         return Response(
        #             {"error": "This campaign does not need that much money."},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )
        #     campaign.steel_needed_money -= amount
        #     campaign.save()

        callback_url = request.build_absolute_uri(reverse("finance:callback_gateway"))
        response_url = generate_payment_url(amount, callback_url)
        url = response_url.get("payment_url").url

        return Response(self.OutputRequestPaymentSerializer({"url": url}).data)

@permission_classes([AllowAny])
class CallbackPaymentUrl(APIView):

    def get(self, request):
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM)

        if not tracking_code:
            return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            return Response({"error": "Tracking code not found"}, status=status.HTTP_404_NOT_FOUND)

        if bank_record.is_success:
            return Response({"message": "پرداخت با موفقیت انجام شد.", "tracking_code": tracking_code}, status=status.HTTP_200_OK)

        return Response(
            {"message": "پرداخت با شکست مواجه شده است. اگر پول کم شده است، ظرف مدت ۴۸ ساعت باز خواهد گشت."},
            status=status.HTTP_400_BAD_REQUEST
        )