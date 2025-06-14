from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import (
    DecyzjaWojtaForm,
    OcenaKomisjiForm,
    RealizacjaSkarbnikaForm,
    WeryfikacjaFormalnaForm,
    WniosekDotacjaForm,
)
from .models import WniosekDotacja


class ZlozWniosekDotacjaView(LoginRequiredMixin, CreateView):
    model = WniosekDotacja
    form_class = WniosekDotacjaForm
    template_name = "dotacje/zloz_wniosek.html"
    success_url = reverse_lazy("ogolne:moje_wnioski")

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)


class ListaWnioskowDotacjeView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = WniosekDotacja
    template_name = "dotacje/lista_wnioskow.html"
    context_object_name = "wnioski"

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=[
                "Urzędnik ds. dotacji",
                "Komisja ds. dotacji",
                "Wójt",
                "Skarbnik gminy",
            ]
        ).exists()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Urzędnik ds. dotacji").exists():
            return WniosekDotacja.objects.filter(
                status__in=["Złożony", "Braki formalne"]
            )
        if user.groups.filter(name="Komisja ds. dotacji").exists():
            return WniosekDotacja.objects.filter(status="Do oceny komisji")
        if user.groups.filter(name="Wójt").exists():
            return WniosekDotacja.objects.filter(status="Do decyzji wójta")
        if user.groups.filter(name="Skarbnik gminy").exists():
            return WniosekDotacja.objects.filter(status="Zatwierdzony")

        return WniosekDotacja.objects.none()


class RozpatrzWniosekDotacjaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WniosekDotacja
    template_name = "dotacje/rozpatrz_wniosek.html"
    context_object_name = "wniosek"
    success_url = reverse_lazy("dotacje:lista_wnioskow")

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=[
                "Urzędnik ds. dotacji",
                "Komisja ds. dotacji",
                "Wójt",
                "Skarbnik gminy",
            ]
        ).exists()

    def get_form_class(self):
        status = self.object.status
        user = self.request.user

        if (
            status in ["Złożony", "Braki formalne"]
            and user.groups.filter(name="Urzędnik ds. dotacji").exists()
        ):
            return WeryfikacjaFormalnaForm

        if (
            status == "Do oceny komisji"
            and user.groups.filter(name="Komisja ds. dotacji").exists()
        ):
            return OcenaKomisjiForm

        if status == "Do decyzji wójta" and user.groups.filter(name="Wójt").exists():
            return DecyzjaWojtaForm

        if (
            status == "Zatwierdzony"
            and user.groups.filter(name="Skarbnik gminy").exists()
        ):
            return RealizacjaSkarbnikaForm

        return forms.Form
