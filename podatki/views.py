# podatki/views.py

from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import DecyzjaPodatkowa, Wplata
from .forms import DecyzjaPodatkowaForm, WplataForm

class NowaDecyzjaPodatkowaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DecyzjaPodatkowa
    form_class = DecyzjaPodatkowaForm
    template_name = 'podatki/nowa_decyzja.html'
    success_url = reverse_lazy('podatki:lista_decyzji')

    def test_func(self):
        return self.request.user.groups.filter(name='urzednik_ds_podatkow').exists()

class ListaDecyzjiView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = DecyzjaPodatkowa
    template_name = 'podatki/lista_decyzji.html'
    context_object_name = 'decyzje'

    def test_func(self):
        return self.request.user.groups.filter(name='urzednik_ds_podatkow').exists()

class RejestrujWplateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Wplata
    form_class = WplataForm
    template_name = 'podatki/rejestruj_wplate.html'
    # Poprawiono success_url
    success_url = reverse_lazy('podatki:lista_decyzji')

    def test_func(self):
        return self.request.user.groups.filter(name='urzednik_ds_podatkow').exists()

    def form_valid(self, form):
        decyzja = DecyzjaPodatkowa.objects.get(pk=self.kwargs['pk'])
        form.instance.decyzja = decyzja
        form.instance.urzednik = self.request.user

        # Oznaczamy decyzję jako opłaconą (uproszczenie)
        decyzja.oplacona = True
        decyzja.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['decyzja'] = DecyzjaPodatkowa.objects.get(pk=self.kwargs['pk'])
        return context