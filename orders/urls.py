from django.urls import path

from .views import order_create_view, order_detail_view

urlpatterns = [
   path('create/', order_create_view, name='order_create'),
   path('detail/<int:order_id>/', order_detail_view, name='order_detail'),
]
