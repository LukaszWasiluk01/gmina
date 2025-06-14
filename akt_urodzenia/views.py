# akt_urodzenia/views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
import random
from datetime import date

from .models import ZgloszenieUrodzenia
from .forms import ZgloszenieUrodzeniaForm, RozpatrzZgloszenieForm

def is_urzednik_rejestru_cywilnego(user):
    return user.groups.filter(name='urzednik_ds_rejestru_stanu_cywilnego').exists()

class ZglosUrodzenieView(LoginRequiredMixin, CreateView):
    model = ZgloszenieUrodzenia
    form_class = ZgloszenieUrodzeniaForm
    template_name = 'akt_urodzenia/zglos_urodzenie.html'
    success_url = reverse_lazy('ogolne:moje_wnioski')

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)

class ListaZgloszenUrodzenView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ZgloszenieUrodzenia
    template_name = 'akt_urodzenia/lista_urodzen.html'
    context_object_name = 'zgloszenia'

    def test_func(self):
        return is_urzednik_rejestru_cywilnego(self.request.user)

class ZgloszenieDetailView(LoginRequiredMixin, DetailView):
    model = ZgloszenieUrodzenia
    template_name = 'akt_urodzenia/rozpatrz_zgloszenie_detail.html'
    context_object_name = 'zgloszenie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Przekazujemy formularz do kontekstu tylko dla urzędnika
        if is_urzednik_rejestru_cywilnego(self.request.user):
            context['form'] = RozpatrzZgloszenieForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        if not is_urzednik_rejestru_cywilnego(request.user):
            return redirect('ogolne:index')

        zgloszenie = self.get_object()
        form = RozpatrzZgloszenieForm(request.POST, instance=zgloszenie)

        if form.is_valid():
            action = request.POST.get("action")
            if action == "accept":
                zgloszenie.status = 'Zaakceptowany'
                zgloszenie.pesel_dziecka = self.generuj_pesel(zgloszenie.data_urodzenia_dziecka, zgloszenie.plec_dziecka)
            elif action == "reject":
                zgloszenie.status = 'Odrzucony'

            form.save()

        return redirect('akt_urodzenia:lista_zgloszen')

    def generuj_pesel(self, data_urodzenia, plec):
        rok = str(data_urodzenia.year)
        miesiac = data_urodzenia.month
        dzien = data_urodzenia.day

        if data_urodzenia.year >= 2000:
            miesiac += 20

        pesel = rok[2:]
        pesel += f"{miesiac:02d}"
        pesel += f"{dzien:02d}"

        # Prosta seria, w rzeczywistości bardziej skomplikowana
        seria = f"{random.randint(100, 999):03d}"
        pesel += seria

        if plec == 'M':
            cyfra_plci = random.choice([1, 3, 5, 7, 9])
        else: # 'K'
            cyfra_plci = random.choice([0, 2, 4, 6, 8])
        pesel += str(cyfra_plci)

        # Prosta suma kontrolna
        wagi = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        suma = 0
        for i in range(10):
            suma += int(pesel[i]) * wagi[i]

        kontrola = (10 - (suma % 10)) % 10
        pesel += str(kontrola)

        return pesel