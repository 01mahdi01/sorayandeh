from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models
from azbankgateways.exceptions import AZBankGatewaysException


def generate_payment_url(amount, callback_url, bank_type=bank_models.BankType.ZARINPAL):
    """
    Generates a payment URL for the specified bank gateway.

    :param amount: Amount in IRR (Rials)
    :param callback_url: The callback URL where the bank redirects after payment
    :param bank_type: The bank gateway type (default is ZarinPal)
    :return: Payment URL or error message
    """
    try:
        bank = bankfactories.BankFactory().create(bank_type)
        bank.set_amount(amount)
        bank.set_client_callback_url(callback_url)
        bank_record = bank.ready()

        return {"payment_url": bank.redirect_gateway()}

    except AZBankGatewaysException as e:
        return {"error": str(e)}
