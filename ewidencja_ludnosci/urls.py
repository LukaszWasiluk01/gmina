# gmina/ewidencja_ludnosci/urls.py

from django.urls import path
# Usunęliśmy import nieistniejącego 'AktualizujStatystykeView'
# Dodaliśmy import 'ListaMieszkancowView', który istnieje w views.py
from .views import GenerujStatystykiView, ListaMieszkancowView

app_name = 'ewidencja_ludnosci'

urlpatterns = [
    # Ścieżka dla urzędnika ds. ewidencji do przeglądania listy mieszkańców
    path('mieszkancy/', ListaMieszkancowView.as_view(), name='lista_mieszkancow'),

    # Ścieżka dla pracownika ds. statystyki do generowania raportu
    path('statystyki/', GenerujStatystykiView.as_view(), name='generuj_statystyki'),

    # Usunęliśmy ścieżkę /aktualizuj/, która powodowała błąd
]