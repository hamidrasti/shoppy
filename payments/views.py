from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import reverse

from shop.models import Product

User = get_user_model()


def make_payment(request, product_id, user_id):
    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
    except User.DoesNotExist:
        return HttpResponse('User not found.', status=404)
    except Product.DoesNotExist:
        return HttpResponse('The product was not found.', status=404)
    amount = product.price.amount
    # set user mobile. we do not have any user mobile yet. so we skip this line
    # user_mobile_number = user.email  # optional

    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create()  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        bank.set_client_callback_url(reverse('gateway-callback'))
        # bank.set_mobile_number(user_mobile_number)  # optional

        bank_record = bank.ready()

        # forward user to bank gateway
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        return HttpResponse(f'Payment failed. Error: {e.__class__.__name__}', status=500)


def gateway_callback(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        return HttpResponse('This link is not valid.', status=404)

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        return HttpResponse('This link is not valid.', status=404)

    # In this part, we have to do the corresponding record
    # or any other appropriate action through the data in the record bank.
    if bank_record.is_success:
        # Payment has been made successfully and the bank has approved.
        # You can redirect the user to the result page or display the result.
        return HttpResponse('Payment was successful.')

    return HttpResponse('Payment failed. If the money is reduced, it will be returned to your account within 48 hours.')
