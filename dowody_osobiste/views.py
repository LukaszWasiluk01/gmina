# gmina/dowody_osobiste/views.py

from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import WniosekDowod

class WnioskodawcaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Wnioskodawca').exists()

class UrzednikDowodowMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Urzędnik ds. wydawania dowodów osobistych').exists()


# POPRAWIONO NAZWĘ KLASY
class ZlozWniosekDowodView(LoginRequiredMixin, WnioskodawcaMixin, CreateView):
    model = WniosekDowod
    fields = ['powod_wydania']
    template_name = 'dowody_osobiste/zloz_wniosek.html'
    success_url = reverse_lazy('ogolne:moje_wnioski')

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)

# POPRAWIONO NAZWĘ KLASY
class ListaWnioskowDowodView(LoginRequiredMixin, UrzednikDowodowMixin, ListView):
    model = WniosekDowod
    template_name = 'dowody_osobiste/lista_wnioskow.html'
    context_object_name = 'wnioski'

    def get_queryset(self):
        return WniosekDowod.objects.filter(status='Złożony')

# POPRAWIONO NAZWĘ KLASY
class RozpatrzWniosekDowodView(LoginRequiredMixin, UrzednikDowodowMixin, UpdateView):
    model = WniosekDowod
    fields = ['status', 'powod_odrzucenia']
    template_name = 'dowody_osobiste/rozpatrz_wniosek.html'
    success_url = reverse_lazy('dowody_osobiste:lista_wnioskow_dowod')