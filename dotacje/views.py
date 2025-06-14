from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .models import WniosekDotacja

# Create your views here.


class WnioskodawcaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Wnioskodawca").exists()


class UrzednikDotacjiMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Urzędnik ds. dotacji").exists()


class KomisjaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Komisja ds. dotacji").exists()


class WojtMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Wójt").exists()


class ZlozWniosekDotacjaView(WnioskodawcaMixin, CreateView):
    model = WniosekDotacja
    fields = ["tytul", "opis", "kwota"]
    template_name = "dotacje/zloz_wniosek.html"
    success_url = reverse_lazy("dotacje:lista")

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)


class ListaWnioskowView(ListView):
    model = WniosekDotacja
    template_name = "dotacje/lista_wnioskow.html"
    context_object_name = "wnioski"


class RozpatrzWniosekKomisjaView(KomisjaMixin, UpdateView):
    model = WniosekDotacja
    fields = ["status"]
    template_name = "dotacje/rozpatrz_wniosek.html"
    success_url = reverse_lazy("dotacje:lista")


class RozpatrzWniosekWojtView(WojtMixin, UpdateView):
    model = WniosekDotacja
    fields = ["status"]
    template_name = "dotacje/rozpatrz_wniosek.html"
    success_url = reverse_lazy("dotacje:lista")


class PrzelejDotacjeView(UrzednikDotacjiMixin, UpdateView):
    model = WniosekDotacja
    fields = ["status"]
    template_name = "dotacje/rozpatrz_wniosek.html"
    success_url = reverse_lazy("dotacje:lista")

    def form_valid(self, form):
        if form.instance.status == "zatwierdzony_wojt":
            form.instance.status = "zrealizowany"
        return super().form_valid(form)
