# gmina/rejestracja_samochodu/urls.py

from django.urls import path
# Poprawiono importy, aby używały szczegółowych nazw widoków
from .views import (
    ZlozWniosekRejestracjaView,
    ListaWnioskowRejestracjaView,
    RozpatrzWniosekRejestracjaView
)

app_name = 'rejestracja_samochodu'

urlpatterns = [
    # Używamy spójnych i szczegółowych nazw widoków i ścieżek
    path('zloz/', ZlozWniosekRejestracjaView.as_view(), name='zloz_wniosek_rejestracja'),
    path('lista/', ListaWnioskowRejestracjaView.as_view(), name='lista_wnioskow_rejestracja'),
    path('rozpatrz/<int:pk>/', RozpatrzWniosekRejestracjaView.as_view(), name='rozpatrz_wniosek_rejestracja'),
]