# lukaszwasiluk01/gmina/gmina-master/budownictwo/urls.py

from django.urls import path
from .views import (
    ZlozWniosekBudowlanyView,
    WniosekZlozonyView,
    PotwierdzWniosekBudowlanyView,
    ListaWnioskowBudowlanychView,
    RozpatrzWniosekBudowlanyView,
    ListaWnioskowDlaInspektoraView, # Dodany import
    DecyzjaInspektoraView
)

app_name = 'budownictwo'

urlpatterns = [
    path('zloz/', ZlozWniosekBudowlanyView.as_view(), name='zloz_wniosek'),
    path('potwierdz/', PotwierdzWniosekBudowlanyView.as_view(), name='potwierdz_wniosek'),
    path('zlozony/', WniosekZlozonyView.as_view(), name='wniosek_zlozony'),

    # URL dla urzędnika ds. budownictwa
    path('lista/', ListaWnioskowBudowlanychView.as_view(), name='lista_wnioskow'),
    path('rozpatrz/<int:pk>/', RozpatrzWniosekBudowlanyView.as_view(), name='rozpatrz_wniosek'),

    # Nowy URL dla inspektora nadzoru
    path('lista-inspektor/', ListaWnioskowDlaInspektoraView.as_view(), name='lista_wnioskow_inspektor'),
    path('decyzja/<int:pk>/', DecyzjaInspektoraView.as_view(), name='decyzja_inspektora'),
]