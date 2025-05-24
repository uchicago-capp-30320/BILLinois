from django.contrib.auth.models import User, BaseUserManager
from django.contrib.auth import logout
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
    
def delete_account(request: HttpRequest) -> HttpResponse:
    """
    Deletes the user's account.

    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: The rendered delete account page.
    """

    if not request.user.is_authenticated:
        return redirect("account_login")

    if request.method == "POST":
        user = request.user
        password = request.POST.get("password")

        if not user.check_password(password):
            messages.error(request, "Incorrect password.")
            return redirect("delete_account")

        try:
            # We need to log out the user in order to delete them
            logout(request)
            user.delete()
            return redirect("account_goodbye")
        
        except Exception as e:
            messages.error(
                request, "An error occurred while deleting your account.")
    
    return render(request, "account/delete_account.html")

def account_goodbye(request: HttpRequest) -> HttpResponse:
    """
    Renders a page to notify the user that their account has been deleted.

    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: The rendered goodbye page.
    """

    return render(request, "account/account_goodbye.html")