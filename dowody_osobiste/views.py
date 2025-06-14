from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .models import WniosekDowod


class ZlozWniosekDowodView(LoginRequiredMixin, CreateView):
    model = WniosekDowod
    fields = ["powod_wydania"]
    template_name = "dowody_osobiste/zloz_wniosek.html"
    success_url = reverse_lazy("ogolne:moje_wnioski")

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)


class ListaWnioskowDowodView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = WniosekDowod
    template_name = "dowody_osobiste/lista_wnioskow.html"
    context_object_name = "wnioski"

    def test_func(self):
        return self.request.user.groups.filter(
            name="Urzędnik ds. wydawania dowodów osobistych"
        ).exists()


class RozpatrzWniosekDowodView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WniosekDowod
    fields = ["status", "uzasadnienie_odrzucenia"]
    template_name = "dowody_osobiste/rozpatrz_wniosek.html"
    context_object_name = "wniosek"
    success_url = reverse_lazy("dowody_osobiste:lista_wnioskow_dowod")

    def test_func(self):
        return self.request.user.groups.filter(
            name="Urzędnik ds. wydawania dowodów osobistych"
        ).exists()
