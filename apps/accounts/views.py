from django.contrib.auth.models import User, BaseUserManager
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect


class CustomUserManager(BaseUserManager):
    """
    Custom implementation of the UserManager class to handle user creation.
    """

    def create_user(self, username: str, email: str, password: str, phone) -> User:
        """
        Creates a new user in the Users table of the database.

        Args:
            username (str): The username.
            email (str): The email address of the user.
            password (str): The user's password.

        Returns:
            Bool: True if the user was created successfully, False otherwise.
        """
        if User.objects.filter(phone=phone).exists():
            print("Phone already exists")
            return False

        user = User.objects.create_user(
            username=username, email=email, password=password, phone=phone
        )
        user.save()
        return True


def make_account_page(request: HttpRequest) -> HttpResponse:
    """
    Renders the account creation page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered account creation page.
    """
    return render(request, "signup.html")

def unsubscribe(request: HttpRequest) -> HttpResponse:
    """
    Renders the unsubscribe view.
    """

    if request.method == "POST":
        user = request.user

        if user.is_subscribed:
            user.is_subscribed = False

            messages.success(
                request, "You have successfully unsubscribed from updates."
            )
            
        else:
            user.is_subscribed = True

            messages.success(
                request, "You have successfully subscribed to updates."
            )
        user.save()

        return redirect(request.META.get("HTTP_REFERER", "favorites"))