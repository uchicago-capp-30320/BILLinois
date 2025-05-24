from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.make_account_page, name="signup"),
    path("unsubscribe/", views.unsubscribe, name="unsubscribe"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("account_goodbye/", views.account_goodbye, name="account_goodbye"),
]
