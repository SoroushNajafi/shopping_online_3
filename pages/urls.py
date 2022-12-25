from django.urls import path

from .views import HomePageView, contact_us_view

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact/', contact_us_view, name='contact_us'),
]
