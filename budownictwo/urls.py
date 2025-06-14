# gmina/budownictwo/urls.py

from django.urls import path
from .views import (
    ZlozWniosekBudowlanyView, WniosekZlozonyView, PotwierdzWniosekBudowlanyView,
    ListaWnioskowBudowlanychView, RozpatrzWniosekBudowlanyView,
    ListaWnioskowDlaInspektoraView, DecyzjaInspektoraView
)

app_name = 'budownictwo'

urlpatterns = [
    # Poprawiono nazwy na bardziej szczegółowe
    path('zloz/', ZlozWniosekBudowlanyView.as_view(), name='zloz_wniosek_budowlany'),
    path('potwierdz/', PotwierdzWniosekBudowlanyView.as_view(), name='potwierdz_wniosek_budowlany'),
    path('zlozony/', WniosekZlozonyView.as_view(), name='wniosek_zlozony_budowlany'),
    path('lista/', ListaWnioskowBudowlanychView.as_view(), name='lista_wnioskow_budowlanych'),
    path('rozpatrz/<int:pk>/', RozpatrzWniosekBudowlanyView.as_view(), name='rozpatrz_wniosek_budowlany'),
    path('lista-inspektor/', ListaWnioskowDlaInspektoraView.as_view(), name='lista_wnioskow_inspektor'),
    path('decyzja/<int:pk>/', DecyzjaInspektoraView.as_view(), name='decyzja_inspektora'),
]