from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import generate_payment_url
from ..campaign.models import Campaign,Participants
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import FinancialLogs


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
        if not request.GET.get('Authority'):
            return Response({"error": "Authority is required."}, status=status.HTTP_400_BAD_REQUEST)
        # tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM)
        try:
            authority = request.GET.get('Authority')
            bank_record = bank_models.Bank.objects.get(reference_number=authority)
            log = FinancialLogs.objects.select_related("campaign","user").get(pk=bank_record.pk)
        except bank_models.Bank.DoesNotExist:
            return Response({"error": "Authority does not exist."}, status=status.HTTP_400_BAD_REQUEST)


        # if not tracking_code:
        #     return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
        #
        # try:
        #     bank_record = bank_models.Bank.objects.select_related("campaign_transaction",).get(tracking_code=tracking_code)
        # except bank_models.Bank.DoesNotExist:
        #     return Response({"error": "Tracking code not found"}, status=status.HTTP_404_NOT_FOUND)
        frontend_base_url="http://62.60.197.167/payment-result.html"
        if bank_record.is_success:
            with transaction.atomic():
                campaign =Campaign.objects.select_for_update().get(id=log.campaign.id)
                user=BaseUser.objects.get(id= log.user.id)
                participant=Participants.objects.create(user=user, campaign=campaign,participation_type="money")
                campaign.participants.add(user)

            success_url = f"{frontend_base_url}/?tracking_code={authority}"
            return HttpResponseRedirect(success_url)
        else:
            campaign =Campaign.objects.select_for_update().get(id=log.campaign.id)
            campaign.steel_needed_money += int(bank_record.amount)
            failure_url = f"{frontend_base_url}?tracking_code={authority}"
            return HttpResponseRedirect(failure_url)


class GetFinancialLogs(APIView):
    class InputFinancialLogsSerializer(serializers.Serializer):
        tracking_code=serializers.CharField()
    class OutputFinancialLogsSerializer(serializers.Serializer):
        user = serializers.CharField(source="user.name", read_only=True)
        campaign = serializers.CharField(source="campaign.title", read_only=True)
        transaction = serializers.CharField(source="campaign.tracking_code", read_only=True)
        class Meta:
            model = FinancialLogs
            fields = ("user","campaign","transaction")

    def post(self, request):
        serializer = self.InputFinancialLogsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        log=FinancialLogs.objects.select_related("campaign","user",'transaction').get(transaction__reference_number=serializer.validated_data["tracking_code"])
        return Response(self.OutputFinancialLogsSerializer(log).data)
