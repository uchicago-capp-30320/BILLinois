from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("bill/<str:bill_number>/", views.bill_page, name="bill_page"),
]
