# podatki/urls.py

from django.urls import path
# Zmieniono 'GenerujDecyzjeView' na poprawną nazwę 'NowaDecyzjaPodatkowaView'
from .views import ListaDecyzjiView, NowaDecyzjaPodatkowaView, RejestrujWplateView

app_name = 'podatki'

urlpatterns = [
    path('lista/', ListaDecyzjiView.as_view(), name='lista_decyzji'),
    # Użyto poprawnej nazwy widoku w ścieżce URL
    path('nowa/', NowaDecyzjaPodatkowaView.as_view(), name='nowa_decyzja'),
    path('wplata/<int:pk>/', RejestrujWplateView.as_view(), name='rejestruj_wplate'),
]