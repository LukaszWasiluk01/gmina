from collections import defaultdict

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as AuthLoginView
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView

from .forms import RejestracjaForm
from .models import Adres, Mieszkaniec


class IndexView(TemplateView):
    template_name = "ogolne/index.html"


class PanelUrzednikaView(LoginRequiredMixin, TemplateView):
    template_name = "ogolne/panel_urzednika.html"


class RejestracjaView(FormView):
    template_name = "ogolne/rejestracja.html"
    form_class = RejestracjaForm
    success_url = reverse_lazy("ogolne:login")

    @transaction.atomic
    def form_valid(self, form):

        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
        )

        adres = Adres.objects.create(
            ulica=form.cleaned_data["ulica"],
            numer_domu=form.cleaned_data["numer_domu"],
            numer_mieszkania=form.cleaned_data["numer_mieszkania"],
            kod_pocztowy=form.cleaned_data["kod_pocztowy"],
            miejscowosc=form.cleaned_data["miejscowosc"],
        )

        Mieszkaniec.objects.create(
            user=user,
            pesel=form.cleaned_data["pesel"],
            data_urodzenia=form.cleaned_data["data_urodzenia"],
            plec=form.cleaned_data["plec"],
            adres_zamieszkania=adres,
            adres_zameldowania=adres,
        )

        return redirect(self.get_success_url())


class LoginView(AuthLoginView):
    template_name = "ogolne/login.html"


class MojeWnioskiView(LoginRequiredMixin, ListView):
    template_name = "ogolne/moje_wnioski.html"
    context_object_name = "wnioski_pogrupowane"

    def get_queryset(self):
        user = self.request.user
        wnioski_pogrupowane = defaultdict(list)

        wniosek_models_apps = [
            ("akt_urodzenia", "ZgloszenieUrodzenia"),
            ("budownictwo", "WniosekBudowlany"),
            ("dotacje", "WniosekDotacja"),
            ("dowody_osobiste", "WniosekDowod"),
            ("odpady", "DeklaracjaSmieciowa"),
            ("rejestracja_samochodu", "WniosekRejestracja"),
            ("ewidencja_zbiornikow", "DeklaracjaZbiornika"),
            ("ewidencja_zbiornikow", "DeklaracjaOproznienia"),
        ]

        for app_label, model_name in wniosek_models_apps:
            model = apps.get_model(app_label, model_name)
            nazwa_grupy = model._meta.verbose_name_plural.title()
            wnioski = model.objects.filter(wnioskodawca=user).order_by("-data_zlozenia")
            if wnioski.exists():
                wnioski_pogrupowane[nazwa_grupy] = list(wnioski)

        return dict(wnioski_pogrupowane)
