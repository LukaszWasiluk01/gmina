# lukaszwasiluk01/gmina/gmina-master/dotacje/views.py

from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import WniosekDotacja
from .forms import WniosekDotacjaForm, WeryfikacjaKomisjiForm, RekomendacjaWojtaForm, PrzelewDotacjiForm

# --- Mixins do kontroli dostępu ---

class WnioskodawcaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Wnioskodawca').exists()

class KomisjaDotacjiMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Komisja ds. dotacji').exists()

class WojtMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Wójt').exists()

class UrzednikDotacjiMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Urzędnik ds. dotacji').exists()

# --- Widoki dla Wnioskodawcy ---

class ZlozWniosekDotacjaView(LoginRequiredMixin, WnioskodawcaMixin, CreateView):
    model = WniosekDotacja
    form_class = WniosekDotacjaForm
    template_name = 'dotacje/zloz_wniosek.html'
    success_url = reverse_lazy('ogolne:moje_wnioski')

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        form.instance.status = 'Złożony'
        return super().form_valid(form)

# --- Widoki dla Komisji ds. dotacji ---

class ListaWnioskowDlaKomisjiView(LoginRequiredMixin, KomisjaDotacjiMixin, ListView):
    model = WniosekDotacja
    template_name = 'dotacje/lista_wnioskow.html'
    context_object_name = 'wnioski'

    def get_queryset(self):
        return WniosekDotacja.objects.filter(status='Złożony')

class WeryfikujWniosekKomisjaView(LoginRequiredMixin, KomisjaDotacjiMixin, UpdateView):
    model = WniosekDotacja
    form_class = WeryfikacjaKomisjiForm
    template_name = 'dotacje/rozpatrz_wniosek.html'
    success_url = reverse_lazy('dotacje:lista_komisja')

# --- Widoki dla Wójta ---

class ListaWnioskowDlaWojtaView(LoginRequiredMixin, WojtMixin, ListView):
    model = WniosekDotacja
    template_name = 'dotacje/lista_wnioskow.html'
    context_object_name = 'wnioski'

    def get_queryset(self):
        return WniosekDotacja.objects.filter(status='W weryfikacji komisji')

class RozpatrzRekomendacjeWojtView(LoginRequiredMixin, WojtMixin, UpdateView):
    model = WniosekDotacja
    form_class = RekomendacjaWojtaForm
    template_name = 'dotacje/rozpatrz_wniosek.html'
    success_url = reverse_lazy('dotacje:lista_wojt')

# --- Widoki dla Urzędnika ds. dotacji ---

class ListaWnioskowDlaUrzednikaView(LoginRequiredMixin, UrzednikDotacjiMixin, ListView):
    model = WniosekDotacja
    template_name = 'dotacje/lista_wnioskow.html'
    context_object_name = 'wnioski'

    def get_queryset(self):
        # Urzędnik widzi wnioski zatwierdzone przez wójta, gotowe do realizacji
        return WniosekDotacja.objects.filter(status='Zatwierdzony')

class PrzelejDotacjeView(LoginRequiredMixin, UrzednikDotacjiMixin, UpdateView):
    model = WniosekDotacja
    form_class = PrzelewDotacjiForm
    template_name = 'dotacje/rozpatrz_wniosek.html'
    success_url = reverse_lazy('dotacje:lista_urzednik')