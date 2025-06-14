# gmina/rejestracja_samochodu/views.py

from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import WniosekRejestracja

class WnioskodawcaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Wnioskodawca').exists()

class UrzednikRejestracjiMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Urzędnik ds. rejestracji samochodów').exists()

# POPRAWIONO NAZWY WIDOKÓW
class ZlozWniosekRejestracjaView(LoginRequiredMixin, WnioskodawcaMixin, CreateView):
    model = WniosekRejestracja
    fields = ['marka_pojazdu', 'model_pojazdu', 'rok_produkcji', 'numer_vin']
    template_name = 'rejestracja_samochodu/zloz_wniosek.html'
    success_url = reverse_lazy('ogolne:moje_wnioski')

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)

class ListaWnioskowRejestracjaView(LoginRequiredMixin, UrzednikRejestracjiMixin, ListView):
    model = WniosekRejestracja
    template_name = 'rejestracja_samochodu/lista_wnioskow.html'
    context_object_name = 'wnioski'

    def get_queryset(self):
        return WniosekRejestracja.objects.filter(status='Złożony')

class RozpatrzWniosekRejestracjaView(LoginRequiredMixin, UrzednikRejestracjiMixin, UpdateView):
    model = WniosekRejestracja
    fields = ['status', 'powod_odrzucenia']
    template_name = 'rejestracja_samochodu/rozpatrz_wniosek.html'
    success_url = reverse_lazy('rejestracja_samochodu:lista_wnioskow_rejestracja')