# dowody_osobiste/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek

class WniosekDowod(Wniosek):
    powod_wydania = models.CharField(max_length=100, choices=[
        ('pierwszy', 'Pierwszy dowód'),
        ('zmiana_danych', 'Zmiana danych'),
        ('utrata', 'Utrata lub uszkodzenie'),
        ('uplyw_terminu', 'Upływ terminu ważności'),
    ])

    class Meta:
        verbose_name = "Wniosek o dowód osobisty"
        verbose_name_plural = "Wnioski o dowód osobisty"

    def __str__(self):
        return f"Wniosek o dowód dla {self.wnioskodawca.username} z powodu: {self.get_powod_wydania_display()}"

    def get_absolute_url(self):
        return reverse('dowody_osobiste:rozpatrz_wniosek_dowod', kwargs={'pk': self.pk})