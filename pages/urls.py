from django.urls import path

from .views import HomePageView, contact_us_view, search_result_view

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact/', contact_us_view, name='contact_us'),
    path('search/', search_result_view, name='search_result'),
]
