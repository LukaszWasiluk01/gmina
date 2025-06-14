from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .models import WniosekRejestracjaSamochodu

# Create your views here.


class WnioskodawcaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Wnioskodawca").exists()


class UrzednikSamochodowyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(
            name="Urzędnik ds. rejestracji samochodów"
        ).exists()


class ZlozWniosekView(WnioskodawcaMixin, CreateView):
    model = WniosekRejestracjaSamochodu
    fields = ["marka", "model", "numer_rejestracyjny"]
    template_name = "rejestracja_samochodu/zloz_wniosek.html"
    success_url = reverse_lazy("rejestracja_samochodu:zloz_wniosek")

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)


class ListaWnioskowView(UrzednikSamochodowyMixin, ListView):
    model = WniosekRejestracjaSamochodu
    template_name = "rejestracja_samochodu/lista_wnioskow.html"
    context_object_name = "wnioski"


class RozpatrzWniosekView(UrzednikSamochodowyMixin, UpdateView):
    model = WniosekRejestracjaSamochodu
    fields = ["status"]
    template_name = "rejestracja_samochodu/zloz_wniosek.html"
    success_url = reverse_lazy("rejestracja_samochodu:lista")
