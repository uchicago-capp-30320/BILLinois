import os
import random

from allauth.account.adapter import DefaultAccountAdapter
from twilio.rest import Client
from apps.accounts.models import PhoneVerification
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        user.phone = form.cleaned_data.get("phone")

        if commit:
            user.save()

        return user

    def set_phone(self, request, user, phone) -> None:
        if not isinstance(user, str):
            user.phone = phone

    def set_phone_verified(self, request, user, phone) -> None:
        if not isinstance(user, str):
            user.phone_verified = True

    def get_phone(self, user) -> tuple:
        return (getattr(user, "phone", ""), False)
    
    def send_verification_code_sms(self, user, code, phone) -> None:
        API_KEY = os.environ.get("TWILIO_API_KEY")
        AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
        FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")

        PhoneVerification.objects.create(
            user=user,
            code=code
        )

        if os.environ.get("PHONE_DEBUG") == "True":
            print(f"Debug: Verification code for {phone} is {code}")
            return
        
        else:
            try:
                client = Client(API_KEY, AUTH_TOKEN)
                client.messages.create(
                    body=f"Your verification code is: {code}",
                    from_=FROM_NUMBER,
                    to=phone
                )
            
            except Exception as e:
                print(f"Error sending SMS: {e}")
    
    def set_phone_verified(self, user, code) -> None:
        cutoff_time = timezone.now()

        verified = PhoneVerification.objects.filter(
            user = user,
            code = code,
            created_at = cutoff_time - timedelta(minutes=10)
        ).order_by("-created_at").first()

        if verified:
            verified.delete()

        user.phone_verified = True
        user.save()