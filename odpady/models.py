# odpady/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek

class DeklaracjaSmieciowa(Wniosek):
    TYP_ZABUDOWY_CHOICES = [
        ('jednorodzinna', 'Zabudowa jednorodzinna'),
        ('wielorodzinna', 'Zabudowa wielorodzinna'),
    ]
    STATUS_CHOICES = [ # Ujednolicono ze statusami w Wniosek, dodając specyficzny status
        ('Złożony', 'Złożony'),
        ('Opłata naliczona', 'Opłata naliczona'),
        ('Odrzucony', 'Odrzucony'),
    ]

    # Zmieniamy pole statusu, aby używało lokalnych choices
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Złożony')
    liczba_mieszkancow = models.PositiveIntegerField()
    typ_zabudowy = models.CharField(max_length=20, choices=TYP_ZABUDOWY_CHOICES)
    oplata = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Deklaracja śmieciowa"
        verbose_name_plural = "Deklaracje śmieciowe"

    def __str__(self):
        return f"Deklaracja śmieciowa nr {self.id} od {self.wnioskodawca.username}"

    def get_absolute_url(self):
        return reverse('odpady:wylicz_oplate', kwargs={'pk': self.pk})