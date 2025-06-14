# gmina/podatki/urls.py

from django.urls import path
# Poprawiono import: 'GenerujDecyzjeView' zamiast 'NowaDecyzjaView'
from .views import ListaDecyzjiView, GenerujDecyzjeView, RejestrujWplateView

app_name = 'podatki'

urlpatterns = [
    path('lista/', ListaDecyzjiView.as_view(), name='lista_decyzji'),
    # Poprawiono użycie widoku na zgodne z importem
    path('nowa/', GenerujDecyzjeView.as_view(), name='nowa_decyzja'),
    path('rejestruj-wplate/<int:decyzja_id>/', RejestrujWplateView.as_view(), name='rejestruj_wplate'),
]