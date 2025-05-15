import os
import random
import logging

from allauth.account.adapter import DefaultAccountAdapter
from twilio.rest import Client
from apps.accounts.models import PhoneVerification
from datetime import timedelta
from django.utils import timezone

logger = logging.getLogger("phone_verification")
test_phones = os.environ.get("TEST_PHONES", "").split(",")


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Overrides for the default account adapter to allow for phone verification
    """

    def save_user(self, request, user, form, commit=True) -> object:
        """
        Saves a user to the database and sets the phone number.
        """
        user = super().save_user(request, user, form, commit=False)

        user.phone = form.cleaned_data.get("phone")

        if commit:
            user.save()

        return user

    def set_phone(self, request, user, phone) -> None:
        """
        Sets the phone number for the user.
        """
        if not isinstance(user, str):
            user.phone = phone

    def get_phone(self, user) -> tuple:
        """
        Returns the phone number for the user.
        """
        return (getattr(user, "phone", ""), False)

    def send_verification_code_sms(self, user, code, phone) -> None:
        """
        Send a verification code to the user's phone number.
        """
        API_KEY = os.environ.get("TWILIO_API_KEY")
        AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
        FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")

        PhoneVerification.objects.create(user=user, code=code)

        # Access SMS code without sending it via text
        if os.environ.get("PHONE_DEBUG") == "True":
            logger.debug(f"Debug: Verification code for {phone} is {code}")
            return

        else:
            try:
                client = Client(API_KEY, AUTH_TOKEN)
                client.messages.create(
                    body=f"Your verification code is: {code}", from_=FROM_NUMBER, to=phone
                )

            except Exception as e:
                print(f"Error sending SMS: {e}")

    def set_phone_verified(self, user, code) -> None:
        cutoff_time = timezone.now()

        # Check if code is valid and not expired
        verified = (
            PhoneVerification.objects.filter(
                user=user, code=code, created_at=cutoff_time - timedelta(minutes=10)
            )
            .order_by("-created_at")
            .first()
        )

        if verified:
            verified.delete()
            user.phone_verified = True
            user.save()
            return True

        return False
