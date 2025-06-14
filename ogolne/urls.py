# gmina/ogolne/urls.py

from django.urls import path
from .views import MojeWnioskiView, PanelUrzednikaView, WniosekDetailView

app_name = 'ogolne'

urlpatterns = [
    # Usunęliśmy ścieżkę do 'index', ponieważ jest teraz w głównym urls.py
    path('moje-wnioski/', MojeWnioskiView.as_view(), name='moje_wnioski'),
    path('wniosek/<int:pk>/', WniosekDetailView.as_view(), name='wniosek_detail'),
    path('panel-urzednika/', PanelUrzednikaView.as_view(), name='panel_urzednika'),
]