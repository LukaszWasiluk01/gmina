# lukaszwasiluk01/gmina/gmina-master/dotacje/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek  # Import bazowego modelu Wniosek

# Model WniosekDotacja dziedziczy teraz po Wniosek
class WniosekDotacja(Wniosek):
    # Lista statusów specyficzna dla tego typu wniosku
    STATUS_CHOICES = [
        ('Złożony', 'Złożony'),
        ('W weryfikacji komisji', 'W weryfikacji komisji'),
        ('Przekazany do wójta', 'Przekazany do wójta'),
        ('Zatwierdzony', 'Zatwierdzony'),
        ('Odrzucony', 'Odrzucony'),
        ('Zrealizowany', 'Zrealizowany')
    ]

    # Pola specyficzne dla wniosku o dotację
    tytul_projektu = models.CharField(max_length=255)
    opis_projektu = models.TextField()
    wnioskowana_kwota = models.DecimalField(max_digits=10, decimal_places=2)

    # Pole 'status', 'wnioskodawca' i 'data_zlozenia' są dziedziczone z Wniosek

    class Meta:
        verbose_name = "Wniosek o dotację"
        verbose_name_plural = "Wnioski o dotacje"

    def __str__(self):
        return self.tytul_projektu

    def get_absolute_url(self):
        # Ta metoda jest kluczowa dla działania linków w panelu "Moje Wnioski"
        return reverse('ogolne:wniosek_detail', kwargs={'pk': self.pk})