from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Sum
from .models import DecyzjaPodatkowa, Wplata
from .forms import DecyzjaPodatkowaForm, WplataForm

def is_urzednik_podatkow(user):
    return user.is_authenticated and user.groups.filter(name="Urzędnik ds. podatków").exists()

class NowaDecyzjaPodatkowaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DecyzjaPodatkowa
    form_class = DecyzjaPodatkowaForm
    template_name = "podatki/nowa_decyzja.html"
    success_url = reverse_lazy("podatki:lista_decyzji")

    def test_func(self):
        return is_urzednik_podatkow(self.request.user)

class ListaDecyzjiView(LoginRequiredMixin, ListView):
    """
    ZMIANA: Inteligentny widok listy. Inne dane dla urzędnika, inne dla mieszkańca.
    """
    model = DecyzjaPodatkowa
    template_name = "podatki/lista_decyzji.html"
    context_object_name = "decyzje"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if is_urzednik_podatkow(user):
            return DecyzjaPodatkowa.objects.all()
        else:
            return DecyzjaPodatkowa.objects.filter(podatnik=user)

class DecyzjaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    NOWY WIDOK: Uniwersalny widok szczegółów decyzji.
    """
    model = DecyzjaPodatkowa
    template_name = 'podatki/decyzja_detail.html'
    context_object_name = 'decyzja'

    def test_func(self):

        decyzja = self.get_object()
        return is_urzednik_podatkow(self.request.user) or decyzja.podatnik == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        decyzja = self.get_object()

        suma_wplat = decyzja.wplaty.aggregate(Sum('kwota_wplaty'))['kwota_wplaty__sum'] or 0
        context['suma_wplat'] = suma_wplat
        context['pozostalo_do_zaplaty'] = decyzja.kwota - suma_wplat
        return context

class RejestrujWplateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Wplata
    form_class = WplataForm
    template_name = "podatki/rejestruj_wplate.html"

    def test_func(self):
        return is_urzednik_podatkow(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["decyzja"] = get_object_or_404(DecyzjaPodatkowa, pk=self.kwargs["decyzja_pk"])
        return context

    def form_valid(self, form):
        """
        ZMIANA: Poprawiona logika oznaczania decyzji jako opłaconej.
        """
        decyzja = get_object_or_404(DecyzjaPodatkowa, pk=self.kwargs["decyzja_pk"])
        form.instance.decyzja = decyzja
        form.instance.urzednik = self.request.user
        form.save()

        suma_wplat = decyzja.wplaty.aggregate(Sum('kwota_wplaty'))['kwota_wplaty__sum'] or 0
        if suma_wplat >= decyzja.kwota:
            decyzja.oplacona = True
            decyzja.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('podatki:decyzja_detail', kwargs={'pk': self.kwargs['decyzja_pk']})