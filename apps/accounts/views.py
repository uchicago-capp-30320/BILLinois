from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def create_user(username: str, email: str, password: str) -> User:
    """
    Creates a new user in the Users table of the database.

    Args:
        username (str): The username.
        email (str): The email address of the user.
        password (str): The user's password;

    Returns:
        Bool: True if the user was created successfully, False otherwise.
    """

    user = User.objects.create_user(username=username, email=email, password=password)
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
