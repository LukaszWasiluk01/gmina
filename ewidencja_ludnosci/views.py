from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import StatystykaLudnosci

# Create your views here.


class UrzednikLudnosciMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(
            name="Urzędnik ds. ewidencji ludności"
        ).exists()


class StatystykMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Pracownik ds. statystyki").exists()


class AktualizujStatystykeView(UrzednikLudnosciMixin, CreateView):
    model = StatystykaLudnosci
    fields = ["liczba_mieszkancow", "liczba_dzieci", "liczba_seniorow"]
    template_name = "ewidencja_ludnosci/aktualizuj_statystyke.html"
    success_url = reverse_lazy("ewidencja_ludnosci:statystyki")


class GenerujStatystykiView(StatystykMixin, ListView):
    model = StatystykaLudnosci
    template_name = "ewidencja_ludnosci/statystyki.html"
    context_object_name = "statystyki"
