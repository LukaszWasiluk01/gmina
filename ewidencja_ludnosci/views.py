# lukaszwasiluk01/gmina/gmina-master/ewidencja_ludnosci/views.py

from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from datetime import date
from ogolne.models import Mieszkaniec

class UrzednikEwidencjiMixin(UserPassesTestMixin):
    """Mixin dla urzędnika ds. ewidencji ludności."""
    def test_func(self):
        return self.request.user.groups.filter(name='Urzędnik ds. ewidencji ludności').exists()

class PracownikStatystykiMixin(UserPassesTestMixin):
    """Mixin dla pracownika ds. statystyki."""
    def test_func(self):
        return self.request.user.groups.filter(name='Pracownik ds. statystyki').exists()

class ListaMieszkancowView(LoginRequiredMixin, UrzednikEwidencjiMixin, ListView):
    model = Mieszkaniec
    template_name = 'ewidencja_ludnosci/lista_mieszkancow.html' # Załóżmy, że taki szablon istnieje
    context_object_name = 'mieszkancy'
    paginate_by = 50

class GenerujStatystykiView(LoginRequiredMixin, PracownikStatystykiMixin, TemplateView):
    template_name = 'ewidencja_ludnosci/statystyki.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pobranie wszystkich aktywnych mieszkańców
        aktywni_mieszkancy = Mieszkaniec.objects.filter(aktywny=True)

        # Obliczenie statystyk
        liczba_mieszkancow = aktywni_mieszkancy.count()
        liczba_kobiet = aktywni_mieszkancy.filter(plec='K').count()
        liczba_mezczyzn = aktywni_mieszkancy.filter(plec='M').count()

        # Obliczenie wieku i podział na grupy wiekowe
        today = date.today()
        dzieci, mlodziez, dorosli, seniorzy = 0, 0, 0, 0
        for m in aktywni_mieszkancy:
            wiek = today.year - m.data_urodzenia.year - ((today.month, today.day) < (m.data_urodzenia.month, m.data_urodzenia.day))
            if wiek < 18:
                dzieci += 1
            elif 18 <= wiek < 26:
                mlodziez += 1
            elif 26 <= wiek < 65:
                dorosli += 1
            else:
                seniorzy += 1

        # Dodanie statystyk do kontekstu
        context['statystyki'] = {
            'liczba_mieszkancow': liczba_mieszkancow,
            'liczba_kobiet': liczba_kobiet,
            'procent_kobiet': round((liczba_kobiet / liczba_mieszkancow * 100), 2) if liczba_mieszkancow else 0,
            'liczba_mezczyzn': liczba_mezczyzn,
            'procent_mezczyzn': round((liczba_mezczyzn / liczba_mieszkancow * 100), 2) if liczba_mieszkancow else 0,
            'grupy_wiekowe': {
                'dzieci': dzieci,
                'mlodziez': mlodziez,
                'dorosli': dorosli,
                'seniorzy': seniorzy,
            }
        }
        return context