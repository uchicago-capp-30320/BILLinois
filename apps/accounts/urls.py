from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.make_account_page, name="signup"),
    path("unsubscribe/", views.unsubscribe, name="unsubscribe"),
]
