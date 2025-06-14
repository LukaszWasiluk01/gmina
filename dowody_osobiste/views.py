from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .models import WniosekDowodowy

# Create your views here.


class WnioskodawcaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Wnioskodawca").exists()


class UrzednikDowodyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(
            name="Urzędnik ds. wydawania dowodów osobistych"
        ).exists()


class ZlozWniosekView(WnioskodawcaMixin, CreateView):
    model = WniosekDowodowy
    fields = ["imie", "nazwisko", "pesel", "adres_zameldowania"]
    template_name = "dowody_osobiste/zloz_wniosek.html"
    success_url = reverse_lazy("dowody_osobiste:lista")

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)


class ListaWnioskowView(ListView):
    model = WniosekDowodowy
    template_name = "dowody_osobiste/lista_wnioskow.html"
    context_object_name = "wnioski"


class RozpatrzWniosekView(UrzednikDowodyMixin, UpdateView):
    model = WniosekDowodowy
    fields = ["status"]
    template_name = "dowody_osobiste/rozpatrz_wniosek.html"
    success_url = reverse_lazy("dowody_osobiste:lista")
