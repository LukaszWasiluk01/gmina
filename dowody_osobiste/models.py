# gmina/dowody_osobiste/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek

class WniosekDowod(Wniosek):
    STATUS_CHOICES = [
        ('Złożony', 'Złożony'),
        ('W trakcie weryfikacji', 'W trakcie weryfikacji'),
        ('Przekazany do PWPW', 'Przekazany do PWPW'),
        ('Do odbioru', 'Do odbioru'),
        ('Odrzucony', 'Odrzucony'),
    ]

    powod_wydania = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Złożony')

    def __str__(self):
        return f"Wniosek o dowód nr {self.id} dla {self.wnioskodawca.username}"

    def get_absolute_url(self):
        return reverse('ogolne:wniosek_detail', kwargs={'pk': self.pk})