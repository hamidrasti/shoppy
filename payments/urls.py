from django.urls import path

from payments.views import gateway_callback, make_payment

urlpatterns = [
    path('pay/<int:product_id>/<int:user_id>/', make_payment),
    path('gateway-callback/', gateway_callback, name='gateway-callback'),
]
