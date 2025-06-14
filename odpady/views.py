from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .models import DeklaracjaSmieciowa

# Create your views here.


class WnioskodawcaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Wnioskodawca").exists()


class UrzednikSmieciMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(
            name="Urzędnik ds. gospodarki odpadami"
        ).exists()


class ZlozDeklaracjeView(WnioskodawcaMixin, CreateView):
    model = DeklaracjaSmieciowa
    fields = ["liczba_osob", "typ_zabudowy"]
    template_name = "odpady/zloz_deklaracje.html"
    success_url = reverse_lazy("odpady:lista")

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)


class ListaDeklaracjiView(ListView):
    model = DeklaracjaSmieciowa
    template_name = "odpady/lista_deklaracji.html"
    context_object_name = "deklaracje"


class WyliczOplateView(UrzednikSmieciMixin, UpdateView):
    model = DeklaracjaSmieciowa
    fields = []
    template_name = "odpady/wylicz_oplate.html"
    success_url = reverse_lazy("odpady:lista")

    def form_valid(self, form):
        deklaracja = form.instance
        if deklaracja.typ_zabudowy == "jednorodzinna":
            oplata = deklaracja.liczba_osob * 25
        else:
            oplata = deklaracja.liczba_osob * 20

        deklaracja.oplata = oplata
        deklaracja.status = "wyliczona"
        return super().form_valid(form)
