# rejestracja_samochodu/views.py

from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import WniosekRejestracja

# Zmieniono nazwy widoków dla spójności
class ZlozWniosekRejestracjaView(LoginRequiredMixin, CreateView):
    model = WniosekRejestracja
    fields = ['marka_pojazdu', 'model_pojazdu', 'rok_produkcji', 'numer_vin']
    template_name = 'rejestracja_samochodu/zloz_wniosek.html'
    success_url = reverse_lazy('ogolne:moje_wnioski')

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)

class ListaWnioskowRejestracjaView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = WniosekRejestracja
    template_name = 'rejestracja_samochodu/lista_wnioskow.html'
    context_object_name = 'wnioski'

    def test_func(self):
        return self.request.user.groups.filter(name='urzednik_ds_rejestracji_samochodow').exists()

class RozpatrzWniosekRejestracjaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WniosekRejestracja
    # Urzędnik może edytować status, uzasadnienie i nadać numer rejestracyjny
    fields = ['status', 'uzasadnienie_odrzucenia', 'numer_rejestracyjny']
    template_name = 'rejestracja_samochodu/rozpatrz_wniosek.html'
    context_object_name = 'wniosek'
    # Poprawiono success_url na poprawną nazwę
    success_url = reverse_lazy('rejestracja_samochodu:lista_wnioskow_rejestracja')

    def test_func(self):
        return self.request.user.groups.filter(name='urzednik_ds_rejestracji_samochodow').exists()