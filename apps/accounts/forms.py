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

    subscribe = forms.BooleanField(
        label="Subscribe to bill updates",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"checked": "checked"}),
    )

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        User = get_user_model()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")

        return email

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get("phone")
        User = get_user_model()

        if phone:
            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError("Phone already exists.")

        return phone

    def save(self, request) -> object:
        User = get_user_model()

        user = User.objects.create_user(
            email=self.cleaned_data.get("email"),
            username=self.cleaned_data.get("email"),
            full_name=self.cleaned_data.get("full_name"),
            is_subscribed=self.cleaned_data.get("subscribe", True),
            phone=self.cleaned_data.get("phone"),
        )

        user.set_password(self.cleaned_data.get("password1"))
        user.save()
        return user