# rejestracja_samochodu/urls.py

from django.urls import path
from .views import (
    ZlozWniosekRejestracjaView,
    ListaWnioskowRejestracjaView,
    RozpatrzWniosekRejestracjaView
)

app_name = 'rejestracja_samochodu'

urlpatterns = [
    # Zaktualizowano ścieżki o nowe, spójne nazwy
    path('zloz/', ZlozWniosekRejestracjaView.as_view(), name='zloz_wniosek_rejestracja'),
    path('lista/', ListaWnioskowRejestracjaView.as_view(), name='lista_wnioskow_rejestracja'),
    path('rozpatrz/<int:pk>/', RozpatrzWniosekRejestracjaView.as_view(), name='rozpatrz_wniosek_rejestracja'),
]