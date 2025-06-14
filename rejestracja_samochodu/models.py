# rejestracja_samochodu/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek

class WniosekRejestracja(Wniosek):
    marka_pojazdu = models.CharField(max_length=100)
    model_pojazdu = models.CharField(max_length=100)
    rok_produkcji = models.PositiveIntegerField()
    numer_vin = models.CharField(max_length=17, unique=True)
    numer_rejestracyjny = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        verbose_name = "Wniosek o rejestrację samochodu"
        verbose_name_plural = "Wnioski o rejestrację samochodów"

    def __str__(self):
        return f"Wniosek o rejestrację {self.marka_pojazdu} {self.model_pojazdu} (VIN: {self.numer_vin})"

    def get_absolute_url(self):
        return reverse('rejestracja_samochodu:rozpatrz_wniosek_rejestracja', kwargs={'pk': self.pk})