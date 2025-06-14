# gmina/dowody_osobiste/urls.py

from django.urls import path
from .views import ZlozWniosekDowodView, ListaWnioskowDowodView, RozpatrzWniosekDowodView

app_name = 'dowody_osobiste'

urlpatterns = [
    # Nazwy są już szczegółowe i poprawne
    path('zloz/', ZlozWniosekDowodView.as_view(), name='zloz_wniosek_dowod'),
    path('lista/', ListaWnioskowDowodView.as_view(), name='lista_wnioskow_dowod'),
    path('rozpatrz/<int:pk>/', RozpatrzWniosekDowodView.as_view(), name='rozpatrz_wniosek_dowod'),
]