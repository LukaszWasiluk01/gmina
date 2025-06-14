# gmina/dotacje/urls.py

from django.urls import path
from .views import (
    ZlozWniosekDotacjaView,
    ListaWnioskowDlaKomisjiView,
    WeryfikujWniosekKomisjaView,
    ListaWnioskowDlaWojtaView,
    RozpatrzRekomendacjeWojtView,
    ListaWnioskowDlaUrzednikaView,
    PrzelejDotacjeView,
)

app_name = 'dotacje'

urlpatterns = [
    # Poprawiono nazwę na 'zloz_wniosek_dotacja'
    path('zloz/', ZlozWniosekDotacjaView.as_view(), name='zloz_wniosek_dotacja'),
    path('lista-komisja/', ListaWnioskowDlaKomisjiView.as_view(), name='lista_komisja'),
    path('weryfikuj-komisja/<int:pk>/', WeryfikujWniosekKomisjaView.as_view(), name='weryfikuj_komisja'),
    path('lista-wojt/', ListaWnioskowDlaWojtaView.as_view(), name='lista_wojt'),
    path('rekomendacja-wojt/<int:pk>/', RozpatrzRekomendacjeWojtView.as_view(), name='rekomendacja_wojt'),
    path('lista-urzednik/', ListaWnioskowDlaUrzednikaView.as_view(), name='lista_urzednik'),
    path('przelej-dotacje/<int:pk>/', PrzelejDotacjeView.as_view(), name='przelej_dotacje'),
]