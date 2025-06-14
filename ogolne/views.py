from django.apps import apps
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from .forms import RejestracjaForm

# Create your views here.


class IndexView(TemplateView):
    template_name = "ogolne/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            group_names = list(user.groups.values_list("name", flat=True))
            context["is_wnioskodawca"] = "Wnioskodawca" in group_names
            context["is_urzednik"] = any(
                [
                    name.startswith("Urzędnik")
                    or name
                    in [
                        "Wójt",
                        "Skarbnik gminy",
                        "Komisja ds. dotacji",
                        "Inspektor nadzoru budowlanego",
                        "Pracownik ds. statystyki",
                    ]
                    for name in group_names
                ]
            )
        return context


class RejestracjaView(CreateView):
    form_class = RejestracjaForm
    template_name = "ogolne/rejestracja.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        group, _ = Group.objects.get_or_create(name="Wnioskodawca")
        self.object.groups.add(group)
        return response


class PanelUrzędnikaView(LoginRequiredMixin, TemplateView):
    template_name = "ogolne/panel_urzednika.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        def in_group(name):
            return user.groups.filter(name=name).exists()

        context.update(
            {
                "is_usc": in_group("Urzędnik ds. rejestru stanu cywilnego"),
                "is_zbiorniki": in_group("Urzędnik ds. ewidencji zbiorników"),
                "is_podatki": in_group("Urzędnik ds. podatków"),
                "is_ludnosc": in_group("Urzędnik ds. ewidencji ludności"),
                "is_statystyka": in_group("Pracownik ds. statystyki"),
                "is_samochody": in_group("Urzędnik ds. rejestracji samochodów"),
                "is_dotacje": in_group("Urzędnik ds. dotacji"),
                "is_komisja_dotacje": in_group("Komisja ds. dotacji"),
                "is_wojt": in_group("Wójt"),
                "is_budownictwo": in_group("Urzędnik ds. budownictwa"),
                "is_inspektor": in_group("Inspektor nadzoru budowlanego"),
                "is_odpady": in_group("Urzędnik ds. gospodarki odpadami"),
                "is_dowody": in_group("Urzędnik ds. wydawania dowodów osobistych"),
            }
        )
        return context


class MojeWnioskiView(LoginRequiredMixin, TemplateView):
    template_name = "ogolne/moje_wnioski.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        wnioski = []
        for app_config in apps.get_app_configs():
            try:
                for model in app_config.get_models():
                    if hasattr(model, "wnioskodawca") and hasattr(
                        model, "data_zlozenia"
                    ):
                        user_wnioski = model.objects.filter(wnioskodawca=user)
                        if user_wnioski.exists():
                            wnioski.append(
                                (
                                    model._meta.verbose_name_plural.title(),
                                    [
                                        {
                                            "instance": w,
                                            "model_name": model._meta.model_name,
                                            "app_label": model._meta.app_label,
                                        }
                                        for w in user_wnioski
                                    ],
                                )
                            )
            except:
                continue

        context["wszystkie_wnioski"] = wnioski
        return context


class WniosekDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "ogolne/wniosek_detail.html"

    def test_func(self):
        obj = self.get_object()
        return obj.wnioskodawca == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied("Nie masz dostępu listy tych wniosków.")

    def get_object(self):
        app_label = self.kwargs["app_label"]
        model_name = self.kwargs["model"]
        pk = self.kwargs["pk"]

        model = apps.get_model(app_label=app_label, model_name=model_name)
        return get_object_or_404(model, pk=pk, wnioskodawca=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        # Pobierz wszystkie pola modelu
        pola = []
        for field in obj._meta.get_fields():
            if field.concrete and not field.many_to_many:
                nazwa = (
                    field.verbose_name.title()
                    if hasattr(field, "verbose_name")
                    else field.name
                )
                wartosc = getattr(obj, field.name)
                pola.append((nazwa, wartosc))
        context["pola_wniosku"] = pola
        return context
