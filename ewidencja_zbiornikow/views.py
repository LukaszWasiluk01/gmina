from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import DeklaracjaOproznienia, DeklaracjaZbiornika

# Create your views here.


class ZadeklarujZbiornikView(LoginRequiredMixin, CreateView):
    model = DeklaracjaZbiornika
    fields = ["tytul", "adres", "pojemnosc_l"]
    template_name = "ewidencja_zbiornikow/zadeklaruj_zbiornik.html"
    success_url = reverse_lazy("ogolne:moje_wnioski")

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)


class ZadeklarujOproznienieView(LoginRequiredMixin, CreateView):
    model = DeklaracjaOproznienia
    fields = ["tytul", "zbiornik", "data_oproznienia"]
    template_name = "ewidencja_zbiornikow/zadeklaruj_oproznienie.html"
    success_url = reverse_lazy("ogolne:moje_wnioski")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["zbiornik"].queryset = DeklaracjaZbiornika.objects.filter(
            wnioskodawca=self.request.user
        )
        return form

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)


class UrzednikTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(
            name="Urzędnik ds. ewidencji zbiorników"
        ).exists()


class ListaDeklaracjiView(UrzednikTestMixin, ListView):
    model = DeklaracjaZbiornika
    template_name = "ewidencja_zbiornikow/lista_deklaracji.html"
    context_object_name = "deklaracje"
