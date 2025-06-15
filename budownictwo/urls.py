from django.urls import path

from .views import (
    ListaWnioskowBudowlanychView,
    PotwierdzWniosekBudowlanyView,
    WniosekBudowlanyDetailView,
    ZlozWniosekBudowlanyView,
)

app_name = "budownictwo"

urlpatterns = [
    path("zloz/", ZlozWniosekBudowlanyView.as_view(), name="zloz_wniosek_budowlany"),
    path(
        "potwierdz/",
        PotwierdzWniosekBudowlanyView.as_view(),
        name="potwierdz_wniosek_budowlany",
    ),
    path(
        "lista/",
        ListaWnioskowBudowlanychView.as_view(),
        name="lista_wnioskow_budowlanych",
    ),
    path("wniosek/<int:pk>/", WniosekBudowlanyDetailView.as_view(), name="wniosek_detail"),
]
