from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import DecyzjaPodatkowa, Wplata

# Create your views here.


class UrzednikPodatkowyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Urzędnik ds. podatków").exists()


class NowaDecyzjaView(UrzednikPodatkowyMixin, CreateView):
    model = DecyzjaPodatkowa
    fields = ["podatnik", "tytul", "kwota"]
    template_name = "podatki/nowa_decyzja.html"
    success_url = reverse_lazy("podatki:lista_decyzji")


class ListaDecyzjiView(UrzednikPodatkowyMixin, ListView):
    model = DecyzjaPodatkowa
    template_name = "podatki/lista_decyzji.html"
    context_object_name = "decyzje"


class RejestrujWplateView(UrzednikPodatkowyMixin, CreateView):
    model = Wplata
    fields = ["decyzja", "kwota"]
    template_name = "podatki/rejestruj_wplate.html"
    success_url = reverse_lazy("podatki:lista_decyzji")
