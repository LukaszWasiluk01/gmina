from django.urls import path

from .views import ListaDecyzjiView, NowaDecyzjaPodatkowaView, RejestrujWplateView

app_name = "podatki"

urlpatterns = [
    path("lista/", ListaDecyzjiView.as_view(), name="lista_decyzji"),
    path("nowa/", NowaDecyzjaPodatkowaView.as_view(), name="nowa_decyzja"),
    path("wplata/<int:pk>/", RejestrujWplateView.as_view(), name="rejestruj_wplate"),
]
