from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("toggle_favorite/<path:bill_id>/", views.toggle_favorite, name="toggle_favorite"),