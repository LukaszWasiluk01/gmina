# dotacje/urls.py

from django.urls import path
from .views import ZlozWniosekDotacjaView, ListaWnioskowDotacjeView, RozpatrzWniosekDotacjaView

app_name = 'dotacje'

urlpatterns = [
    # Poprawiono literówkę w ścieżce
    path('zloz/', ZlozWniosekDotacjaView.as_view(), name='zloz_wniosek_dotacja'),
    path('lista/', ListaWnioskowDotacjeView.as_view(), name='lista_wnioskow'),
    path('rozpatrz/<int:pk>/', RozpatrzWniosekDotacjaView.as_view(), name='rozpatrz_wniosek'),
]