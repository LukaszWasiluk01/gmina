from django.urls import path

from .views import (
    ListaWnioskowDowodView,
    RozpatrzWniosekDowodView,
    ZlozWniosekDowodView,
)

app_name = "dowody_osobiste"

urlpatterns = [
    path("zloz/", ZlozWniosekDowodView.as_view(), name="zloz_wniosek_dowod"),
    path("lista/", ListaWnioskowDowodView.as_view(), name="lista_wnioskow_dowod"),
    path(
        "rozpatrz/<int:pk>/",
        RozpatrzWniosekDowodView.as_view(),
        name="rozpatrz_wniosek_dowod",
    ),
]
