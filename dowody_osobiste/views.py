from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView

from .models import WniosekDowod
from .forms import WniosekDowodForm, RozpatrzWniosekDowodForm

def is_urzednik_dowodow(user):
    return user.is_authenticated and user.groups.filter(name="Urzędnik ds. wydawania dowodów osobistych").exists()

class ZlozWniosekDowodView(LoginRequiredMixin, CreateView):
    model = WniosekDowod
    form_class = WniosekDowodForm
    template_name = "dowody_osobiste/zloz_wniosek.html"
    success_url = reverse_lazy("ogolne:moje_wnioski")

    def form_valid(self, form):
        form.instance.wnioskodawca = self.request.user
        return super().form_valid(form)

class ListaWnioskowDowodView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = WniosekDowod
    template_name = "dowody_osobiste/lista_wnioskow.html"
    context_object_name = "wnioski"
    paginate_by = 10

    def test_func(self):
        return is_urzednik_dowodow(self.request.user)

    def get_queryset(self):

        return WniosekDowod.objects.filter(status="Złożony")

class WniosekDowodDetailView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    ZAKTUALIZOWANY, UNIWERSALNY WIDOK SZCZEGÓŁÓW.
    """
    model = WniosekDowod
    form_class = RozpatrzWniosekDowodForm
    template_name = "dowody_osobiste/wniosek_detail.html"
    context_object_name = "wniosek"

    def test_func(self):
        """Dostęp ma właściciel wniosku LUB urzędnik."""
        wniosek = self.get_object()
        return wniosek.wnioskodawca == self.request.user or is_urzednik_dowodow(self.request.user)

    def get_context_data(self, **kwargs):
        """Dodaje formularz do kontekstu tylko dla urzędnika."""
        context = super().get_context_data(**kwargs)
        if not is_urzednik_dowodow(self.request.user):
            context['form'] = None
        return context

    def form_valid(self, form):
        """Ustawia status na podstawie klikniętego przycisku."""
        action = self.request.POST.get("action")
        wniosek = form.save(commit=False)

        if action == "accept":
            wniosek.status = "Przekazany do PWPW"
        elif action == "reject":
            wniosek.status = "Odrzucony"

        wniosek.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("dowody_osobiste:lista_wnioskow_dowod")