import json
import requests

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from orders.models import Order
from django.conf import settings


def payment_process(request):
    # get order id form session to pay
    order_id = request.session.get('order_id')

    # get order object
    order = get_object_or_404(Order, id=order_id)

    total_price = order.get_total_price()
    rial_total_price = total_price * 10

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        'accept': 'application/json',
        'content_type': 'application/json',
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'Order no.{order.id} : {order.user.first_name} {order.user.last_name}',
        'callback_url': 'http://127.0.0.1:8000',
    }

    response = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = response.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')

    else:
        return HttpResponse('Error from zarinpal')
