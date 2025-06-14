# budownictwo/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek, Adres # Import Adres z aplikacji ogolne

class WniosekBudowlany(Wniosek):
    # Usunięto zduplikowany model Adres, używamy tego z 'ogolne'
    adres_inwestycji = models.ForeignKey(Adres, on_delete=models.CASCADE)
    rodzaj_inwestycji = models.CharField(max_length=200)
    numer_dzialki = models.CharField(max_length=50)
    # Dodano brakujące pola, które były używane w szablonach
    tytul = models.CharField(max_length=255, default="Wniosek o pozwolenie na budowę")
    opis_budowy = models.TextField()

    class Meta:
        verbose_name = "Wniosek budowlany"
        verbose_name_plural = "Wnioski budowlane"

    def __str__(self):
        return f"Wniosek budowlany nr {self.id} dla działki {self.numer_dzialki}"

    def get_absolute_url(self):
        # Url do widoku szczegółowego dla urzędnika lub wnioskodawcy
        return reverse('budownictwo:rozpatrz_wniosek', kwargs={'pk': self.pk})