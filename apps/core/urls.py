from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path(
        "toggle_favorite/<path:bill_id>/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    path("favorites/", views.favorites_page, name="favorites_page"),
    path(
        "bill/<str:state>/<str:session>/<str:bill_number>/",
        views.bill_page,
        name="bill_by_info",
    ),
    path("bill/<path:bill_id>/", views.bill_page, name="bill_by_id"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
]
