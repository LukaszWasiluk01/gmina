# gmina/dotacje/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek  # WAŻNE: Importujemy bazowy model Wniosek

# WAŻNE: Zmieniamy dziedziczenie z models.Model na Wniosek
class WniosekDotacja(Wniosek):
    # Definiujemy statusy specyficzne dla tego wniosku.
    STATUS_CHOICES = [
        ('Złożony', 'Złożony'),
        ('W weryfikacji komisji', 'W weryfikacji komisji'),
        ('Przekazany do wójta', 'Przekazany do wójta'),
        ('Zatwierdzony', 'Zatwierdzony'),
        ('Odrzucony', 'Odrzucony'),
        ('Zrealizowany', 'Zrealizowany')
    ]

    # Pola specyficzne tylko dla wniosku o dotację
    tytul_projektu = models.CharField(max_length=255)
    opis_projektu = models.TextField()
    wnioskowana_kwota = models.DecimalField(max_digits=10, decimal_places=2)

    # Pola 'wnioskodawca' i 'status' są teraz dziedziczone, więc ich tu nie powtarzamy.

    class Meta:
        verbose_name = "Wniosek o dotację"
        verbose_name_plural = "Wnioski o dotacje"

    def __str__(self):
        return self.tytul_projektu

    def get_absolute_url(self):
        return reverse('ogolne:wniosek_detail', kwargs={'pk': self.pk})