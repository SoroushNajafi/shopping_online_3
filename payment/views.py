from django.shortcuts import render, get_object_or_404

from orders.models import Order


def payment_process(request):
    # get order id form session to pay
    order_id = request.session.get('order_id')

    # get order object
    order = get_object_or_404(Order, id=order_id)

    total_price = order.get_total_price()
    rial_total_price = total_price * 10

