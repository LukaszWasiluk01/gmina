# lukaszwasiluk01/gmina/gmina-master/dowody_osobiste/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek  # Import bazowego modelu Wniosek

# Model WniosekDowod dziedziczy teraz po Wniosek
class WniosekDowod(Wniosek):
    # Lista statusów specyficzna dla tego typu wniosku
    STATUS_CHOICES = [
        ('Złożony', 'Złożony'),
        ('W trakcie weryfikacji', 'W trakcie weryfikacji'),
        ('Przekazany do PWPW', 'Przekazany do PWPW'),
        ('Do odbioru', 'Do odbioru'),
        ('Odrzucony', 'Odrzucony'),
    ]

    # Pole specyficzne dla wniosku o dowód
    powod_wydania = models.CharField(max_length=255)

    # Pola 'status', 'wnioskodawca' i 'data_zlozenia' są dziedziczone z Wniosek

    class Meta:
        verbose_name = "Wniosek o dowód osobisty"
        verbose_name_plural = "Wnioski o dowody osobiste"

    def __str__(self):
        return f"Wniosek o dowód nr {self.id} dla {self.wnioskodawca.username}"

    def get_absolute_url(self):
        # Ta metoda jest kluczowa dla działania linków w panelu "Moje Wnioski"
        return reverse('ogolne:wniosek_detail', kwargs={'pk': self.pk})