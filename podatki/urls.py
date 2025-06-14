from django.urls import path

from .views import ListaDecyzjiView, NowaDecyzjaView, RejestrujWplateView

app_name = "podatki"

urlpatterns = [
    path("nowa/", NowaDecyzjaView.as_view(), name="nowa_decyzja"),
    path("lista/", ListaDecyzjiView.as_view(), name="lista_decyzji"),
    path("wplata/", RejestrujWplateView.as_view(), name="rejestruj_wplate"),
]
