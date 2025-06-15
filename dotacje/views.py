from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView

from .models import WniosekDotacja
from .forms import (
    WniosekDotacjaForm,
    RozpatrzWniosekDotacjaForm
)

def is_urzednik_dotacji(user):
    return user.is_authenticated and user.groups.filter(name="Urzędnik ds. dotacji").exists()

def is_komisja(user):
    return user.is_authenticated and user.groups.filter(name="Komisja ds. dotacji").exists()

def is_wojt(user):
    return user.is_authenticated and user.groups.filter(name="Wójt").exists()

def is_skarbnik(user):
    return user.is_authenticated and user.groups.filter(name="Skarbnik gminy").exists()

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
            name__in=["Urzędnik ds. dotacji", "Komisja ds. dotacji", "Wójt", "Skarbnik gminy"]
        ).exists()

    def get_queryset(self):
        user = self.request.user
        if is_urzednik_dotacji(user):
            return WniosekDotacja.objects.filter(status__in=["Złożony"])
        if is_komisja(user):
            return WniosekDotacja.objects.filter(status="Do oceny komisji")
        if is_wojt(user):
            return WniosekDotacja.objects.filter(status="Do decyzji wójta")
        if is_skarbnik(user):
            return WniosekDotacja.objects.filter(status="Do realizacji (Skarbnik)")
        return WniosekDotacja.objects.none()

class WniosekDotacjaDetailView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WniosekDotacja
    form_class = RozpatrzWniosekDotacjaForm
    template_name = "dotacje/wniosek_detail.html"
    context_object_name = "wniosek"
    success_url = reverse_lazy("dotacje:lista_wnioskow")

    def test_func(self):
        wniosek = self.get_object()
        user = self.request.user
        return (
            wniosek.wnioskodawca == user
            or is_urzednik_dotacji(user)
            or is_komisja(user)
            or is_wojt(user)
            or is_skarbnik(user)
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['status'] = self.object.status
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        status = self.object.status
        show_form = (
            (is_urzednik_dotacji(user) and status in ["Złożony"]) or
            (is_komisja(user) and status == "Do oceny komisji") or
            (is_wojt(user) and status == "Do decyzji wójta") or
            (is_skarbnik(user) and status == "Do realizacji (Skarbnik)")
        )
        if not show_form:
            context['form'] = None
        return context

    def form_valid(self, form):
        action = self.request.POST.get("action")
        user = self.request.user
        wniosek = form.save(commit=False)

        if is_urzednik_dotacji(user):
            if action == "accept": wniosek.status = "Do oceny komisji"
            elif action == "reject": wniosek.status = "Odrzucony"

        elif is_komisja(user):
            if action == "accept": wniosek.status = "Do decyzji wójta"
            elif action == "reject": wniosek.status = "Odrzucony"

        elif is_wojt(user):
            if action == "accept": wniosek.status = "Do realizacji (Skarbnik)"
            elif action == "reject": wniosek.status = "Odrzucony"

        elif is_skarbnik(user):
            if action == "accept": wniosek.status = "Zrealizowany"

        wniosek.save()
        return redirect(self.get_success_url())