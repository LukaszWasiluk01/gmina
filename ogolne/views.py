# lukaszwasiluk01/gmina/gmina-master/ogolne/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import chain
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from .forms import RejestracjaForm

# Importowanie wszystkich modeli wniosków z całego projektu
from akt_urodzenia.models import ZgloszenieUrodzenia
from budownictwo.models import WniosekBudowlany
from dotacje.models import WniosekDotacja
from dowody_osobiste.models import WniosekDowod
from ewidencja_zbiornikow.models import DeklaracjaOproznienia, DeklaracjaZbiornika
from odpady.models import DeklaracjaSmieciowa
from rejestracja_samochodu.models import WniosekRejestracja

class IndexView(TemplateView):
    template_name = 'ogolne/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Sprawdzenie czy użytkownik jest w jakiejkolwiek grupie oprócz "Wnioskodawca"
            is_urzednik = self.request.user.groups.exclude(name='Wnioskodawca').exists()
            context['is_urzednik'] = is_urzednik
        return context

class RejestracjaView(CreateView):
    form_class = RejestracjaForm
    template_name = 'ogolne/rejestracja.html'
    success_url = reverse_lazy('ogolne:login')

class PanelUrzednikaView(LoginRequiredMixin, TemplateView):
    template_name = 'ogolne/panel_urzednika.html'

class MojeWnioskiView(LoginRequiredMixin, ListView):
    template_name = 'ogolne/moje_wnioski.html'
    context_object_name = 'wnioski'

    def get_queryset(self):
        user = self.request.user
        # Zbieranie zapytań (querysets) dla każdego typu wniosku
        zgloszenia_urodzen = ZgloszenieUrodzenia.objects.filter(wnioskodawca=user)
        wnioski_budowlane = WniosekBudowlany.objects.filter(wnioskodawca=user)
        wnioski_dotacje = WniosekDotacja.objects.filter(wnioskodawca=user)
        wnioski_dowody = WniosekDowod.objects.filter(wnioskodawca=user)
        deklaracje_oproznienia = DeklaracjaOproznienia.objects.filter(wnioskodawca=user)
        deklaracje_zbiornika = DeklaracjaZbiornika.objects.filter(wnioskodawca=user)
        deklaracje_smieciowe = DeklaracjaSmieciowa.objects.filter(wnioskodawca=user)
        wnioski_rejestracja = WniosekRejestracja.objects.filter(wnioskodawca=user)

        # Użycie itertools.chain do połączenia wszystkich wyników w jedną listę
        # a następnie posortowanie jej według daty złożenia (od najnowszych)
        wszystkie_wnioski = sorted(
            chain(
                zgloszenia_urodzen, wnioski_budowlane, wnioski_dotacje,
                wnioski_dowody, deklaracje_oproznienia, deklaracje_zbiornika,
                deklaracje_smieciowe, wnioski_rejestracja
            ),
            key=lambda wniosek: wniosek.data_zlozenia,
            reverse=True
        )
        return wszystkie_wnioski

class WniosekDetailView(LoginRequiredMixin, DetailView):
    template_name = 'ogolne/wniosek_detail.html'
    context_object_name = 'wniosek'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')

        # Lista wszystkich modeli wniosków do przeszukania
        models = [
            ZgloszenieUrodzenia, WniosekBudowlany, WniosekDotacja, WniosekDowod,
            DeklaracjaOproznienia, DeklaracjaZbiornika, DeklaracjaSmieciowa, WniosekRejestracja
        ]

        # Pętla przez modele w poszukiwaniu obiektu o danym PK, który należy do użytkownika
        for model in models:
            try:
                obj = get_object_or_404(model, pk=pk, wnioskodawca=self.request.user)
                return obj
            except model.DoesNotExist:
                continue # Jeśli nie znaleziono w tym modelu, przejdź do następnego

        # Jeśli obiekt nie zostanie znaleziony w żadnym z modeli, zwróć None (co spowoduje błąd 404)
        return None