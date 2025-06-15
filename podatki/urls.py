from django.urls import path
from .views import (
    NowaDecyzjaPodatkowaView,
    ListaDecyzjiView,
    DecyzjaDetailView,
    RejestrujWplateView
)

app_name = "podatki"

urlpatterns = [
    path("lista/", ListaDecyzjiView.as_view(), name="lista_decyzji"),
    path("nowa/", NowaDecyzjaPodatkowaView.as_view(), name="nowa_decyzja"),

    path("decyzja/<int:pk>/", DecyzjaDetailView.as_view(), name="decyzja_detail"),
    path("decyzja/<int:decyzja_pk>/rejestruj-wplate/", RejestrujWplateView.as_view(), name="rejestruj_wplate"),
]