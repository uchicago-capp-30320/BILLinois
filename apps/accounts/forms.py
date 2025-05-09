from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django import forms


class CustomSignupForm(SignupForm):
    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        User = get_user_model()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        
        return email

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get("phone")
        User = get_user_model()

        if User.objects.filter(phone=phone).exists():
            print("Phone exists")
            raise forms.ValidationError("Phone already exists.")
        
        return phone
