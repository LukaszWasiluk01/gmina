# budownictwo/views.py

from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from .models import WniosekBudowlany, Adres
from .forms import WniosekBudowlanyForm, RozpatrzWniosekForm, DecyzjaInspektoraForm

def is_urzednik_budownictwa(user):
    return user.groups.filter(name='urzednik_ds_budownictwa').exists()

def is_inspektor(user):
    return user.groups.filter(name='inspektor_nadzoru_budowlanego').exists()

class ZlozWniosekBudowlanyView(LoginRequiredMixin, CreateView):
    model = WniosekBudowlany
    form_class = WniosekBudowlanyForm
    template_name = 'budownictwo/zloz_wniosek_budowlany.html'

    def form_valid(self, form):
        # Nie zapisujemy jeszcze, tylko tworzymy obiekty w pamięci
        adres_data = {
            'ulica': form.cleaned_data['ulica'],
            'numer_domu': form.cleaned_data['numer_domu'],
            'numer_mieszkania': form.cleaned_data['numer_mieszkania'],
            'kod_pocztowy': form.cleaned_data['kod_pocztowy'],
            'miejscowosc': form.cleaned_data['miejscowosc'],
        }
        wniosek_data = {
            'tytul': form.cleaned_data['tytul'],
            'opis_budowy': form.cleaned_data['opis_budowy'],
            'rodzaj_inwestycji': form.cleaned_data['rodzaj_inwestycji'],
            'numer_dzialki': form.cleaned_data['numer_dzialki'],
        }

        # Przechowujemy dane w sesji do potwierdzenia
        self.request.session['wniosek_budowlany_data'] = wniosek_data
        self.request.session['adres_inwestycji_data'] = adres_data

        # Poprawiono przekierowanie na poprawną nazwę URL
        return HttpResponseRedirect(reverse_lazy('budownictwo:potwierdz_wniosek_budowlany'))

class PotwierdzWniosekBudowlanyView(LoginRequiredMixin, CreateView):
    template_name = 'budownictwo/potwierdz_wniosek_budowlany.html'
    model = WniosekBudowlany
    form_class = WniosekBudowlanyForm # Potrzebne, żeby szablon miał dostęp do pól

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wniosek_data'] = self.request.session.get('wniosek_budowlany_data')
        context['adres_data'] = self.request.session.get('adres_inwestycji_data')
        return context

    def post(self, request, *args, **kwargs):
        wniosek_data = request.session.get('wniosek_budowlany_data')
        adres_data = request.session.get('adres_inwestycji_data')

        if not wniosek_data or not adres_data:
            return redirect('budownictwo:zloz_wniosek_budowlany')

        adres = Adres.objects.create(**adres_data)
        wniosek = WniosekBudowlany.objects.create(
            wnioskodawca=request.user,
            adres_inwestycji=adres,
            **wniosek_data
        )

        # Czyszczenie sesji
        del request.session['wniosek_budowlany_data']
        del request.session['adres_inwestycji_data']

        return redirect('ogolne:moje_wnioski')

class ListaWnioskowBudowlanychView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = WniosekBudowlany
    template_name = 'budownictwo/lista_wnioskow.html'
    context_object_name = 'wnioski'

    def test_func(self):
        return is_urzednik_budownictwa(self.request.user) or is_inspektor(self.request.user)

    def get_queryset(self):
        if is_inspektor(self.request.user):
            # Inspektor widzi tylko wnioski zaakceptowane przez urzędnika
            return WniosekBudowlany.objects.filter(status='W weryfikacji')
        return WniosekBudowlany.objects.all()

class RozpatrzWniosekBudowlanyView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WniosekBudowlany
    form_class = RozpatrzWniosekForm
    template_name = 'budownictwo/rozpatrz_wniosek.html'
    context_object_name = 'wniosek'
    # Poprawiono success_url
    success_url = reverse_lazy('budownictwo:lista_wnioskow_budowlanych')

    def test_func(self):
        return is_urzednik_budownictwa(self.request.user)

class DecyzjaInspektoraView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WniosekBudowlany
    form_class = DecyzjaInspektoraForm
    template_name = 'budownictwo/decyzja_inspektora.html'
    context_object_name = 'wniosek'
    # Poprawiono success_url
    success_url = reverse_lazy('budownictwo:lista_wnioskow_budowlanych')

    def test_func(self):
        return is_inspektor(self.request.user)