# lukaszwasiluk01/gmina/gmina-master/podatki/views.py

from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import DecyzjaPodatkowa, Wplata
from .forms import DecyzjaPodatkowaForm, WplataForm

class UrzednikPodatkowyMixin(UserPassesTestMixin):
    """Mixin sprawdzający, czy użytkownik jest w grupie urzędników ds. podatków."""
    def test_func(self):
        return self.request.user.groups.filter(name='Urzędnik ds. podatków').exists()

class ListaDecyzjiView(LoginRequiredMixin, UrzednikPodatkowyMixin, ListView):
    model = DecyzjaPodatkowa
    template_name = 'podatki/lista_decyzji.html'
    context_object_name = 'decyzje'
    paginate_by = 20

class GenerujDecyzjeView(LoginRequiredMixin, UrzednikPodatkowyMixin, CreateView):
    model = DecyzjaPodatkowa
    form_class = DecyzjaPodatkowaForm
    template_name = 'podatki/nowa_decyzja.html'
    success_url = reverse_lazy('podatki:lista_decyzji')

class RejestrujWplateView(LoginRequiredMixin, UrzednikPodatkowyMixin, CreateView):
    model = Wplata
    form_class = WplataForm
    template_name = 'podatki/rejestruj_wplate.html'
    success_url = reverse_lazy('podatki:lista_decyzji')

    def get_initial(self):
        # Ustawia początkową wartość pola 'decyzja' na podstawie URL
        decyzja_id = self.kwargs.get('decyzja_id')
        return {'decyzja': decyzja_id}

    def form_valid(self, form):
        # Przypisuje zalogowanego urzędnika do wpłaty
        form.instance.urzednik_rejestrujacy = self.request.user

        # Opcjonalnie: Aktualizacja statusu decyzji po zarejestrowaniu wpłaty
        wplata = form.save()
        decyzja = wplata.decyzja

        # Sprawdzenie, czy suma wpłat pokrywa kwotę decyzji
        suma_wplat = sum(w.kwota_wplaty for w in decyzja.wplaty.all())
        if suma_wplat >= decyzja.kwota:
            decyzja.czy_oplacona = True
            decyzja.save()

        return super().form_valid(form)