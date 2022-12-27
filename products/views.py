from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Product, Comment, Category
from .forms import CommentForm


class ProductsByCategoryListView(generic.ListView):
    model = Category
    template_name = 'products/products_By_category.html'

    def get_queryset(self):
        category_id = int(self.kwargs['category_id'])
        category = get_object_or_404(Category, id=category_id)
        return category.products.all()

    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = int(self.kwargs['category_id'])
        category = get_object_or_404(Category, id=category_id)
        context['category'] = category
        return context


class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/products_list.html'
    queryset = Product.objects.filter(active=True)
    context_object_name = 'products'


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        product_id = int(self.kwargs['product_id'])
        product = get_object_or_404(Product, id=product_id)
        obj.product = product
        messages.success(self.request, _('Your comment added successfully'))
        return super().form_valid(form)


class CommentUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Comment
    template_name = 'products/comment_update.html'
    fields = ['body', 'stars']
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

