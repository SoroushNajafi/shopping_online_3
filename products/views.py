from django.views import generic

from .models import Product


class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/products_list.html'
    queryset = Product.objects.filter(active=True)
    context_object_name = 'products'


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


