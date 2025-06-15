from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, FormView

from .forms import RozpatrzWniosekForm, WniosekBudowlanyForm
from .models import Adres, WniosekBudowlany


def is_urzednik_budownictwa(user):
    return user.groups.filter(name="Urzędnik ds. budownictwa").exists()


def is_inspektor(user):
    return user.groups.filter(name="Inspektor nadzoru budowlanego").exists()


class ZlozWniosekBudowlanyView(LoginRequiredMixin, FormView):
    template_name = 'budownictwo/zloz_wniosek_budowlany.html'
    form_class = WniosekBudowlanyForm

    def get_initial(self):
        initial_data = {}
        wniosek_data = self.request.session.get('wniosek_budowlany_data', {})
        adres_data = self.request.session.get('adres_inwestycji_data', {})
        initial_data.update(wniosek_data)
        initial_data.update(adres_data)
        return initial_data

    def form_valid(self, form):
        adres_fields = ['ulica', 'numer_domu', 'numer_mieszkania', 'kod_pocztowy', 'miejscowosc']
        wniosek_fields = ['tytul', 'opis_budowy', 'rodzaj_inwestycji', 'numer_dzialki']
        adres_data = {field: form.cleaned_data[field] for field in adres_fields}
        wniosek_data = {field: form.cleaned_data[field] for field in wniosek_fields}
        self.request.session['wniosek_budowlany_data'] = wniosek_data
        self.request.session['adres_inwestycji_data'] = adres_data
        return redirect('budownictwo:potwierdz_wniosek_budowlany')

class PotwierdzWniosekBudowlanyView(LoginRequiredMixin, TemplateView):
    template_name = "budownictwo/potwierdz_wniosek_budowlany.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wniosek_data"] = self.request.session.get("wniosek_budowlany_data")
        context["adres_data"] = self.request.session.get("adres_inwestycji_data")
        return context

    def post(self, request, *args, **kwargs):
        wniosek_data = request.session.get("wniosek_budowlany_data")
        adres_data = request.session.get("adres_inwestycji_data")
        if not wniosek_data or not adres_data:
            return redirect("budownictwo:zloz_wniosek_budowlany")
        adres = Adres.objects.create(**adres_data)
        WniosekBudowlany.objects.create(
            wnioskodawca=request.user,
            adres_inwestycji=adres,
            **wniosek_data
        )
        del request.session["wniosek_budowlany_data"]
        del request.session["adres_inwestycji_data"]
        return redirect("ogolne:moje_wnioski")


class ListaWnioskowBudowlanychView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = WniosekBudowlany
    template_name = "budownictwo/lista_wnioskow.html"
    context_object_name = "wnioski"

    def test_func(self):
        return is_urzednik_budownictwa(self.request.user) or is_inspektor(self.request.user)

    def get_queryset(self):
        if is_inspektor(self.request.user):
            return WniosekBudowlany.objects.filter(status="W weryfikacji")
        return WniosekBudowlany.objects.filter(status="Złożony")


class WniosekBudowlanyDetailView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WniosekBudowlany
    form_class = RozpatrzWniosekForm
    template_name = "budownictwo/wniosek_detail.html"
    context_object_name = "wniosek"

    def test_func(self):
        wniosek = self.get_object()
        user = self.request.user
        return (
            wniosek.wnioskodawca == user
            or is_urzednik_budownictwa(user)
            or is_inspektor(user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        wniosek = self.get_object()

        show_form = False
        if is_urzednik_budownictwa(user) and wniosek.status == 'Złożony':
            show_form = True
        elif is_inspektor(user) and wniosek.status == 'W weryfikacji':
            show_form = True

        if not show_form:
            context['form'] = None

        return context

    def form_valid(self, form):
        action = self.request.POST.get("action")
        user = self.request.user
        wniosek = form.instance

        if is_urzednik_budownictwa(user):
            if action == "accept":
                wniosek.status = "W weryfikacji"
            elif action == "reject":
                wniosek.status = "Odrzucony"

        elif is_inspektor(user):
            if action == "accept":
                wniosek.status = "Zaakceptowany"
            elif action == "reject":
                wniosek.status = "Odrzucony"

        wniosek.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("budownictwo:lista_wnioskow_budowlanych")