# ewidencja_ludnosci/views.py

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Poprawiono import, aby używał właściwej nazwy modelu: StatystykaLudnosci
from .models import StatystykaLudnosci

class GenerujStatystykiView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    # Zmieniono widok na ListView, który jest przeznaczony do wyświetlania listy obiektów z modelu.

    # Ustawiono poprawny model
    model = StatystykaLudnosci
    template_name = 'ewidencja_ludnosci/statystyki.html'

    # Nazwa, pod którą lista obiektów będzie dostępna w szablonie
    context_object_name = 'statystyki'

    # Sortujemy od najnowszych statystyk
    ordering = ['-data']

    def test_func(self):
        """Sprawdza, czy użytkownik ma uprawnienia do oglądania statystyk."""
        return self.request.user.groups.filter(name='pracownik_ds_statystyki').exists()