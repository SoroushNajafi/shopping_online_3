from django.urls import path

from .views import ProductListView, ProductDetailView, CommentCreateView, ProductsByCategoryListView, CommentUpdateView

urlpatterns = [
    path('', ProductListView.as_view(), name='products_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('comment/<int:product_id>/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/update/<int:comment_id>/', CommentUpdateView.as_view(), name='comment_update'),
    path('category/<int:category_id>/', ProductsByCategoryListView.as_view(), name='products_by_category'),
]
