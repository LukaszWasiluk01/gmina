from django.urls import path
from .views import (
    ZlozWniosekDowodView,
    ListaWnioskowDowodView,
    WniosekDowodDetailView,
)

app_name = "dowody_osobiste"

urlpatterns = [
    path("zloz/", ZlozWniosekDowodView.as_view(), name="zloz_wniosek_dowod"),
    path("lista/", ListaWnioskowDowodView.as_view(), name="lista_wnioskow_dowod"),

    path("wniosek/<int:pk>/", WniosekDowodDetailView.as_view(), name="wniosek_detail"),
]