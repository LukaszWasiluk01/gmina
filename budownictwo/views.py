# lukaszwasiluk01/gmina/gmina-master/budownictwo/views.py

from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import WniosekBudowlany
from .forms import WniosekBudowlanyForm, WeryfikujWniosekBudowlanyForm, DecyzjaInspektoraForm


class WnioskodawcaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Wnioskodawca').exists()

class UrzednikBudowlanyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Urzędnik ds. budownictwa').exists()

class InspektorNadzoruMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Inspektor nadzoru budowlanego').exists()

class ZlozWniosekBudowlanyView(LoginRequiredMixin, WnioskodawcaMixin, FormView):
    template_name = 'budownictwo/zloz_wniosek_budowlany.html'
    form_class = WniosekBudowlanyForm

    def form_valid(self, form):
        self.request.session['wniosek_budowlany_data'] = form.cleaned_data
        return redirect('budownictwo:potwierdz_wniosek')

class PotwierdzWniosekBudowlanyView(LoginRequiredMixin, WnioskodawcaMixin, TemplateView):
    template_name = 'budownictwo/potwierdz_wniosek_budowlany.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wniosek_data'] = self.request.session.get('wniosek_budowlany_data')
        return context

    def post(self, request, *args, **kwargs):
        wniosek_data = request.session.get('wniosek_budowlany_data')
        if wniosek_data:
            form = WniosekBudowlanyForm(wniosek_data)
            if form.is_valid():
                wniosek = form.save(commit=False)
                wniosek.wnioskodawca = request.user
                wniosek.save()
                del request.session['wniosek_budowlany_data']
                return redirect('budownictwo:wniosek_zlozony')
        return redirect('budownictwo:zloz_wniosek')

class WniosekZlozonyView(LoginRequiredMixin, TemplateView):
    template_name = 'budownictwo/wniosek_zlozony.html'

class ListaWnioskowBudowlanychView(LoginRequiredMixin, UrzednikBudowlanyMixin, ListView):
    model = WniosekBudowlany
    template_name = 'budownictwo/lista_wnioskow.html'
    context_object_name = 'wnioski'

    def get_queryset(self):
        # Urzędnik ds. budownictwa widzi tylko nowe, niezwerfikowane wnioski
        return WniosekBudowlany.objects.filter(status='Złożony')

class RozpatrzWniosekBudowlanyView(LoginRequiredMixin, UrzednikBudowlanyMixin, UpdateView):
    model = WniosekBudowlany
    form_class = WeryfikujWniosekBudowlanyForm
    template_name = 'budownictwo/rozpatrz_wniosek.html'
    success_url = reverse_lazy('budownictwo:lista_wnioskow')

class ListaWnioskowDlaInspektoraView(LoginRequiredMixin, InspektorNadzoruMixin, ListView):
    model = WniosekBudowlany
    template_name = 'budownictwo/lista_wnioskow.html'
    context_object_name = 'wnioski'

    def get_queryset(self):
        # Inspektor nadzoru widzi tylko wnioski, które zostały zweryfikowane przez urzędnika
        return WniosekBudowlany.objects.filter(status='Zweryfikowany')

class DecyzjaInspektoraView(LoginRequiredMixin, InspektorNadzoruMixin, UpdateView):
    model = WniosekBudowlany
    form_class = DecyzjaInspektoraForm
    template_name = 'budownictwo/decyzja_inspektora.html'
    success_url = reverse_lazy('budownictwo:lista_wnioskow_inspektor')