import json
import requests

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _

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
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback')),
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


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    total_price = order.get_total_price()
    rial_total_price = total_price * 10

    if payment_status == 'OK':
        request_header = {
            'accept': 'application/json',
            'content_type': 'application/json',
        }

        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': rial_total_price,
            'authority': payment_authority,
        }
        response = requests.post(url='https://api.zarinpal.com/pg/v4/payment/verify.json',
                                 data=json.dumps(request_data),
                                 headers=request_header,
                                 )

        if 'data' in response.json() and ('errors' not in response.json()['data'] or len(response.json()['data']['errors']) == 0):
            data = response.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('your payment was successful.')

            elif payment_code == 101:
                return HttpResponse('You have done the payment before, this payment is duplicate.')

            else:
                errors_code = response.json()['errors']['code']
                errors_message = response.json()['errors']['message']
                return HttpResponse(f'failure in payment;{errors_code}-{errors_message}')

    else:
        return HttpResponse(f'failure in payment')


def payment_process_sandbox(request):
    # get order id form session to pay
    order_id = request.session.get('order_id')

    # get order object
    order = get_object_or_404(Order, id=order_id)

    total_price = order.get_total_price()
    rial_total_price = total_price * 10

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

    request_header = {
        'accept': 'application/json',
        'content_type': 'application/json',
    }

    request_data = {
        'MerchantID': 'aaabbbaaabbbaaabbbaaabbbaaabbbaaabbb',
        'Amount': rial_total_price,
        'Description': f'Order no.{order.id} : {order.user.first_name} {order.user.last_name}',
        'CallbackURL': request.build_absolute_uri(reverse('payment:payment_callback')),
    }

    response = requests.post(url=zarinpal_request_url, json=request_data, headers=request_header)

    data = response.json()
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))

    else:
        errors = data['errors']
        messages.error(request, _('Error from zarinpal'))
        return render(request, 'payment/error_from_zarinpal.html', {'errors': errors})


def payment_callback_sandbox(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    total_price = order.get_total_price()
    rial_total_price = total_price * 10

    if payment_status == 'OK':
        request_header = {
            'accept': 'application/json',
            'content_type': 'application/json',
        }

        request_data = {
            'MerchantID': 'aaabbbaaabbbaaabbbaaabbbaaabbbaaabbb',
            'Amount': rial_total_price,
            'Authority': payment_authority,
        }
        response = requests.post(url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json',
                                 json=request_data,
                                 headers=request_header,
                                 )

        if 'errors' not in response.json():
            data = response.json()
            payment_code = data['Status']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['RefID']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('your payment was successful.')

            elif payment_code == 101:
                return HttpResponse('You have done the payment before, this payment is duplicate.')

            else:
                errors_code = response.json()['errors']['code']
                errors_message = response.json()['errors']['message']
                return HttpResponse(f'failure in payment;{errors_code}-{errors_message}')

    else:
        return HttpResponse(f'failure in payment')
