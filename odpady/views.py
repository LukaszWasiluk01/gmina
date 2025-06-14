# odpady/views.py

from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import DeklaracjaSmieciowa

class ZlozDeklaracjeView(LoginRequiredMixin, CreateView):
    model = DeklaracjaSmieciowa
    # Poprawiono nazwy pól, aby pasowały do modelu
    fields = ['liczba_mieszkancow', 'typ_zabudowy']
    template_name = 'odpady/zloz_deklaracje.html'
    success_url = reverse_lazy('ogolne:moje_wnioski')

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)

class ListaDeklaracjiView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DeklaracjaSmieciowa
    template_name = 'odpady/lista_deklaracji.html'
    context_object_name = 'deklaracje'

    def test_func(self):
        return self.request.user.groups.filter(name='urzednik_ds_gospodarki_odpadami').exists()

class WyliczOplateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DeklaracjaSmieciowa
    fields = ['oplata'] # Tylko to pole edytujemy
    template_name = 'odpady/wylicz_oplate.html'
    context_object_name = 'deklaracja'
    success_url = reverse_lazy('odpady:lista_deklaracji')

    def test_func(self):
        return self.request.user.groups.filter(name='urzednik_ds_gospodarki_odpadami').exists()

    def form_valid(self, form):
        deklaracja = form.save(commit=False)
        # Uproszczone wyliczenie opłaty
        stawka_za_osobe = 30.50
        deklaracja.oplata = deklaracja.liczba_mieszkancow * stawka_za_osobe
        # Poprawiono status na zgodny z modelem
        deklaracja.status = 'Opłata naliczona'
        deklaracja.save()
        return super().form_valid(form)