from django.urls import path

from .views import (
    ListaDeklaracjiView,
    ZadeklarujOproznienieView,
    ZadeklarujZbiornikView,
)

app_name = "ewidencja_zbiornikow"

urlpatterns = [
    path("zbiornik/", ZadeklarujZbiornikView.as_view(), name="zadeklaruj_zbiornik"),
    path(
        "oproznienie/",
        ZadeklarujOproznienieView.as_view(),
        name="zadeklaruj_oproznienie",
    ),
    path("lista/", ListaDeklaracjiView.as_view(), name="lista_deklaracji"),
]
