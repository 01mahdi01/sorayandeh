from django.db import transaction
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import generate_payment_url
from ..campaign.models import Campaign,Participants
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)

from ..users.models import BaseUser


class RequestPaymentUrl(APIView):
    class InputRequestPaymentSerializer(serializers.Serializer):
        amount = serializers.IntegerField()
        campaign_id = serializers.IntegerField()

    class OutputRequestPaymentSerializer(serializers.Serializer):
        url = serializers.URLField()

    def post(self, request):
        serializer = self.InputRequestPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]
        with transaction.atomic():
            campaign = Campaign.objects.select_for_update().get(pk=serializer.validated_data["campaign_id"])
            if amount > campaign.steel_needed_money:
                return Response(
                    {"error": "This campaign does not need that much money."}, status=status.HTTP_400_BAD_REQUEST
                )
            campaign.steel_needed_money -= amount
            campaign.save()

        callback_url = request.build_absolute_uri(reverse("finance:callback_gateway"))
        user = request.user

        response_url = generate_payment_url(amount=amount, callback_url=callback_url, user=user, campaign=campaign,request=request)

        # d = {}

        # for k, v in params.items():
        #     d["name"] = value

        return Response(response_url)


@permission_classes([AllowAny])
class CallbackPaymentUrl(APIView):

    def get(self, request):
        print(100*'f')
        # tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM)
        authority = request.GET.get('Authority')
        print(authority)
        bank_record = bank_models.Bank.objects.select_related("transactions", ).get(reference_number=authority)
        # if not tracking_code:
        #     return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
        #
        # try:
        #     bank_record = bank_models.Bank.objects.select_related("campaign_transaction",).get(tracking_code=tracking_code)
        # except bank_models.Bank.DoesNotExist:
        #     return Response({"error": "Tracking code not found"}, status=status.HTTP_404_NOT_FOUND)

        if bank_record.is_success:
            with transaction.atomic():
                campaign =Campaign.objects.select_for_update().get(id=bank_record.campaign_transaction.campaign)
                user=BaseUser.objects.get(id= bank_record.campaign_transaction.user)
                participant=Participants.objects.create(user=user, campaign=campaign,participation_type="money")
                campaign.participants.add(user)

            return Response(
                {"message": "پرداخت با موفقیت انجام شد.", "tracking_code": bank_record.tracking_code}, status=status.HTTP_200_OK
            )
        else:
            campaign =Campaign.objects.select_for_update().get(id=bank_record.campaign_transaction.campaign)
            campaign.amount += bank_record.amount
            return Response(
                {"message": "پرداخت با شکست مواجه شده است. اگر پول کم شده است، ظرف مدت ۴۸ ساعت باز خواهد گشت."},
                status=status.HTTP_400_BAD_REQUEST,
            )


