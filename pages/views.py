from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views import generic
from django.contrib.auth.decorators import login_required

from .forms import ContactUsForm, MyProfileForm
from products.models import Product
from orders.models import Order, OrderItem


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


def contact_us_view(request):
    contact_us_form = ContactUsForm()

    if request.method == 'GET':
        return render(request, 'pages/contact_us.html', {'contact_us_form': contact_us_form})
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

        return render(request, 'pages/contact_us.html', {'contact_us_form': contact_us_form})


def search_result_view(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        products = Product.objects.filter(Q(title__icontains=query) | Q(category__en_title__icontains=query))
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'pages/search_result.html', {'query': query, 'page_obj': page_obj})


# class SearchResult(generic.ListView):
#     template_name = 'pages/search_result.html'
#     paginate_by = 3
#     context_object_name = 'products'
#
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         return Product.objects.filter(Q(title__icontains=query) | Q(category__en_title__icontains=query))
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         query = self.request.GET.get('q')
#         context['query'] = query
#         return context
@login_required()
def my_profile_view(request):
    profile_form = MyProfileForm()
    user = request.user

    if request.method == 'GET':
        orders = Order.objects.filter(user_id=request.user.id).filter(is_paid=True)
        return render(request, 'pages/my_profile.html', {'orders': orders, 'profile_form': profile_form})

    elif request.method == 'POST':
        profile_form = MyProfileForm(request.POST, instance=user)

        if profile_form.is_valid():
            profile_obj = profile_form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, _('your information is now up to date'))
            return redirect('my_profile')

        return render(request, 'pages/my_profile.html', {'form': profile_form})
