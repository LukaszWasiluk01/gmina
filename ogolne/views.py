# ogolne/views.py

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
# Zmieniono import: usunięto CreateView, dodano FormView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db import transaction
from django.apps import apps
from collections import defaultdict

from .forms import RejestracjaForm
from .models import Mieszkaniec, Adres

class IndexView(TemplateView):
    template_name = 'ogolne/index.html'

class PanelUrzednikaView(LoginRequiredMixin, TemplateView):
    template_name = 'ogolne/panel_urzednika.html'

# Zmieniono klasę bazową z CreateView na FormView
class RejestracjaView(FormView):
    template_name = 'ogolne/rejestracja.html'
    form_class = RejestracjaForm
    success_url = reverse_lazy('ogolne:login')

    @transaction.atomic
    def form_valid(self, form):
        """
        Ta metoda działa identycznie w FormView jak i w CreateView.
        Przetwarza poprawny formularz, tworząc User, Adres i Mieszkaniec.
        """
        # 1. Tworzenie obiektu User
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email']
        )

        # 2. Tworzenie obiektu Adres
        adres = Adres.objects.create(
            ulica=form.cleaned_data['ulica'],
            numer_domu=form.cleaned_data['numer_domu'],
            numer_mieszkania=form.cleaned_data['numer_mieszkania'],
            kod_pocztowy=form.cleaned_data['kod_pocztowy'],
            miejscowosc=form.cleaned_data['miejscowosc']
        )

        # 3. Tworzenie obiektu Mieszkaniec i łączenie go z User i Adres
        Mieszkaniec.objects.create(
            user=user,
            pesel=form.cleaned_data['pesel'],
            data_urodzenia=form.cleaned_data['data_urodzenia'],
            plec=form.cleaned_data['plec'],
            adres_zamieszkania=adres,
            adres_zameldowania=adres  # Domyślnie ustawiamy ten sam adres
        )

        return redirect(self.get_success_url())


class LoginView(AuthLoginView):
    template_name = 'ogolne/login.html'


class MojeWnioskiView(LoginRequiredMixin, ListView):
    template_name = 'ogolne/moje_wnioski.html'
    context_object_name = 'wnioski_pogrupowane'

    def get_queryset(self):
        user = self.request.user
        wnioski_pogrupowane = defaultdict(list)

        # Lista modeli dziedziczących po Wniosek
        wniosek_models_apps = [
            ('akt_urodzenia', 'ZgloszenieUrodzenia'),
            ('budownictwo', 'WniosekBudowlany'),
            ('dotacje', 'WniosekDotacja'),
            ('dowody_osobiste', 'WniosekDowod'),
            ('odpady', 'DeklaracjaSmieciowa'),
            ('rejestracja_samochodu', 'WniosekRejestracja'),
            ('ewidencja_zbiornikow', 'DeklaracjaZbiornika'),
            ('ewidencja_zbiornikow', 'DeklaracjaOproznienia'),
        ]

        for app_label, model_name in wniosek_models_apps:
            model = apps.get_model(app_label, model_name)
            nazwa_grupy = model._meta.verbose_name_plural.title()
            wnioski = model.objects.filter(wnioskodawca=user).order_by('-data_zlozenia')
            if wnioski.exists():
                wnioski_pogrupowane[nazwa_grupy] = list(wnioski)

        return dict(wnioski_pogrupowane)