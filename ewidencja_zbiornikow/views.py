# ewidencja_zbiornikow/views.py

from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import DeklaracjaZbiornika, DeklaracjaOproznienia
from ogolne.models import Adres

class ZadeklarujZbiornikView(LoginRequiredMixin, CreateView):
    model = DeklaracjaZbiornika
    # Poprawiono nazwy pól na zgodne z modelem
    fields = ['adres_nieruchomosci', 'pojemnosc_zbiornika']
    template_name = 'ewidencja_zbiornikow/zadeklaruj_zbiornik.html'
    success_url = reverse_lazy('ogolne:moje_wnioski')

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)

class ZadeklarujOproznienieView(LoginRequiredMixin, CreateView):
    model = DeklaracjaOproznienia
    fields = ['deklaracja_zbiornika', 'data_oproznienia', 'ilosc_sciekow']
    template_name = 'ewidencja_zbiornikow/zadeklaruj_oproznienie.html'
    success_url = reverse_lazy('ogolne:moje_wnioski')

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrujemy, żeby użytkownik mógł wybrać tylko swoje zadeklarowane zbiorniki
        form.fields['deklaracja_zbiornika'].queryset = DeklaracjaZbiornika.objects.filter(wnioskodawca=self.request.user)
        return form

class ListaDeklaracjiZbiornikowView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DeklaracjaOproznienia # Główny model do przeglądania
    template_name = 'ewidencja_zbiornikow/lista_deklaracji.html'
    context_object_name = 'deklaracje'

    def test_func(self):
        return self.request.user.groups.filter(name='urzednik_ds_ewidencji_zbiornikow').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deklaracje_posiadania'] = DeklaracjaZbiornika.objects.all()
        return context