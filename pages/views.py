from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.contrib import messages
from django.db.models import Q

from .forms import ContactUsForm
from products.models import Product
from orders.models import Order, OrderItem


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


def contact_us_view(request):
    if request.method == 'GET':
        return render(request, 'pages/contact_us.html', {'contact_us_form': ContactUsForm()})
    else:
        contact_us_form = ContactUsForm(request.POST)
        if contact_us_form.is_valid():
            cleaned_data = contact_us_form.cleaned_data
            sent_name = cleaned_data['name']
            sent_email = cleaned_data['email']
            send_mail(_('Thank you for contacting us'),
                      _(f'Hi {sent_name}, you contacted us with {sent_email}, we will reach back to you soon.'),
                      None,
                      [sent_email],
                      fail_silently=False,
                      )

            contact_us_form.save()
            messages.success(request, _('your message has been sent successfully.'))
            return redirect('home')

        form_errors = contact_us_form.errors
        return render(request, 'pages/contact_us.html', {'form_errors': form_errors})


def search_result_view(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        # products = get_object_or_404(Product, title__in=query) #in khato mishe jaye khate payin nevesht?
        products = Product.objects.filter(Q(title__icontains=query) | Q(category__en_title__icontains=query))
        return render(request, 'pages/search_result.html', {'products': products})


def my_profile_view(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user_id=request.user.id).filter(is_paid=True)
        return render(request, 'pages/my_profile.html', {'orders': orders})
