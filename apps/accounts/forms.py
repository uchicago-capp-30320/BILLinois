from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model


class CustomSignupForm(SignupForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")
        User = get_user_model()

        existing = User.objects.filter(email=email).first()
        if existing:
            print(f"Auto-deleting user with email {email}")
            existing.delete()

        return email
