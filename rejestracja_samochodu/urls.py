from django.urls import path

from .views import (
    ListaWnioskowRejestracjaView,
    RozpatrzWniosekRejestracjaView,
    ZlozWniosekRejestracjaView,
)

app_name = "rejestracja_samochodu"

urlpatterns = [
    path(
        "zloz/", ZlozWniosekRejestracjaView.as_view(), name="zloz_wniosek_rejestracja"
    ),
    path(
        "lista/",
        ListaWnioskowRejestracjaView.as_view(),
        name="lista_wnioskow_rejestracja",
    ),
    path(
        "rozpatrz/<int:pk>/",
        RozpatrzWniosekRejestracjaView.as_view(),
        name="rozpatrz_wniosek_rejestracja",
    ),
]
