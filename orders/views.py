from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views import generic

from .forms import OrderForm
from cart.cart import Cart
from .models import OrderItem, Order


@login_required
def order_create_view(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _('You can not proceed to checkout because your cart is empty'))
        return redirect('products_list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order_obj,
                    product=item['product_obj'],
                    quantity=item['quantity'],
                    price=item['product_obj'].price,
                )
            cart.clear()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()

            request.session['order_id'] = order_obj.id
            return redirect('payment:payment_process')

    return render(request, 'orders/order_create.html', {'order_form': order_form})


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})
