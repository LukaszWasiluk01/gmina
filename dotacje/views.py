# dotacje/views.py

from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django import forms

from .models import WniosekDotacja
from .forms import (
    WniosekDotacjaForm, WeryfikacjaFormalnaForm, OcenaKomisjiForm,
    DecyzjaWojtaForm, RealizacjaSkarbnikaForm
)

class ZlozWniosekDotacjaView(LoginRequiredMixin, CreateView):
    model = WniosekDotacja
    form_class = WniosekDotacjaForm
    template_name = 'dotacje/zloz_wniosek.html'
    success_url = reverse_lazy('ogolne:moje_wnioski')

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)

class ListaWnioskowDotacjeView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = WniosekDotacja
    template_name = 'dotacje/lista_wnioskow.html'
    context_object_name = 'wnioski'

    def test_func(self):
        """Sprawdza, czy użytkownik należy do którejkolwiek z grup uprawnionych do obsługi dotacji."""
        return self.request.user.groups.filter(name__in=[
            'urzednik_ds_dotacji', 'komisja_ds_dotacji', 'wojt', 'skarbnik_gminy'
        ]).exists()

    def get_queryset(self):
        """Filtruje wnioski, aby każdy urzędnik widział tylko te na swoim etapie pracy."""
        user = self.request.user
        if user.groups.filter(name='urzednik_ds_dotacji').exists():
            return WniosekDotacja.objects.filter(status__in=['Złożony', 'Braki formalne'])
        if user.groups.filter(name='komisja_ds_dotacji').exists():
            return WniosekDotacja.objects.filter(status='Do oceny komisji')
        if user.groups.filter(name='wojt').exists():
            return WniosekDotacja.objects.filter(status='Do decyzji wójta')
        if user.groups.filter(name='skarbnik_gminy').exists():
            return WniosekDotacja.objects.filter(status='Zatwierdzony')

        # Jeśli użytkownik nie ma przypisanej żadnej z ról, nie widzi żadnych wniosków.
        return WniosekDotacja.objects.none()

class RozpatrzWniosekDotacjaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WniosekDotacja
    template_name = 'dotacje/rozpatrz_wniosek.html'
    context_object_name = 'wniosek'
    success_url = reverse_lazy('dotacje:lista_wnioskow')

    def test_func(self):
        """Logika dostępu jest taka sama jak w widoku listy."""
        return self.request.user.groups.filter(name__in=[
            'urzednik_ds_dotacji', 'komisja_ds_dotacji', 'wojt', 'skarbnik_gminy'
        ]).exists()

    def get_form_class(self):
        """
        Dynamicznie wybiera odpowiedni formularz na podstawie aktualnego statusu wniosku
        oraz roli zalogowanego użytkownika. To jest serce logiki workflow.
        """
        status = self.object.status
        user = self.request.user

        if status in ['Złożony', 'Braki formalne'] and user.groups.filter(name='urzednik_ds_dotacji').exists():
            return WeryfikacjaFormalnaForm

        if status == 'Do oceny komisji' and user.groups.filter(name='komisja_ds_dotacji').exists():
            return OcenaKomisjiForm

        if status == 'Do decyzji wójta' and user.groups.filter(name='wojt').exists():
            return DecyzjaWojtaForm

        if status == 'Zatwierdzony' and user.groups.filter(name='skarbnik_gminy').exists():
            return RealizacjaSkarbnikaForm

        # Jeśli dla danego statusu i użytkownika nie ma przewidzianej akcji,
        # zwracamy pusty formularz, który niczego nie wyświetli.
        return forms.Form