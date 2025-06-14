# lukaszwasiluk01/gmina/gmina-master/rejestracja_samochodu/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek  # Import bazowego modelu Wniosek

# Model WniosekRejestracja dziedziczy teraz po Wniosek
class WniosekRejestracja(Wniosek):
    STATUS_CHOICES = [
        ('Złożony', 'Złożony'),
        ('W trakcie weryfikacji', 'W trakcie weryfikacji'),
        ('Zatwierdzony', 'Zatwierdzony'),
        ('Odrzucony', 'Odrzucony'),
    ]

    marka_pojazdu = models.CharField(max_length=100)
    model_pojazdu = models.CharField(max_length=100)
    rok_produkcji = models.PositiveIntegerField()
    numer_vin = models.CharField(max_length=17)

    # Pola 'status', 'wnioskodawca' i 'data_zlozenia' są dziedziczone z Wniosek

    class Meta:
        verbose_name = "Wniosek o rejestrację samochodu"
        verbose_name_plural = "Wnioski o rejestrację samochodu"

    def __str__(self):
        return f"{self.marka_pojazdu} {self.model_pojazdu} ({self.numer_vin})"

    def get_absolute_url(self):
        # Link do ogólnego widoku szczegółów wniosku
        return reverse('ogolne:wniosek_detail', kwargs={'pk': self.pk})