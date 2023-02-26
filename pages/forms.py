from django import forms
from django.contrib.auth import get_user_model

from .models import Contact


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


class MyProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
