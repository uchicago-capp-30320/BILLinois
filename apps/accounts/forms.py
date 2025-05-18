from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django import forms


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(
        label="Full Name",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Full Name"}),
    )

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        user = get_user_model()

        if user.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")

        return email

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get("phone")
        user = get_user_model()

        if phone:
            if user.objects.filter(phone=phone).exists():
                raise forms.ValidationError("Phone already exists.")

        return phone

    def save(self, request) -> object:
        user = super().save(request)
        user.full_name = self.cleaned_data.get("full_name")
        user.save()
        return user
