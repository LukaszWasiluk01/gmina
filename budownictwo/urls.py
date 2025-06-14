from django.urls import path

from .views import (
    DecyzjaInspektoraView,
    ListaWnioskowBudowlanychView,
    PotwierdzWniosekBudowlanyView,
    RozpatrzWniosekBudowlanyView,
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
    path(
        "rozpatrz/<int:pk>/",
        RozpatrzWniosekBudowlanyView.as_view(),
        name="rozpatrz_wniosek",
    ),
    path(
        "decyzja/<int:pk>/", DecyzjaInspektoraView.as_view(), name="decyzja_inspektora"
    ),
]
