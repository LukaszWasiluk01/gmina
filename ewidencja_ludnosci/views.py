from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from .models import StatystykaLudnosci


class GenerujStatystykiView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = StatystykaLudnosci
    template_name = "ewidencja_ludnosci/statystyki.html"

    context_object_name = "statystyki"

    ordering = ["-data"]

    def test_func(self):
        return self.request.user.groups.filter(name="Pracownik ds. statystyki").exists()
