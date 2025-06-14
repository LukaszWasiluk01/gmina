# lukaszwasiluk01/gmina/gmina-master/odpady/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek  # Import bazowego modelu Wniosek

# Model DeklaracjaSmieciowa dziedziczy po Wniosek, traktując deklarację jako rodzaj wniosku
class DeklaracjaSmieciowa(Wniosek):
    STATUS_CHOICES = [
        ('Złożona', 'Złożona'),
        ('Opłata naliczona', 'Opłata naliczona'),
    ]

    TYP_ZABUDOWY_CHOICES = [
        ('jednorodzinna', 'Zabudowa jednorodzinna'),
        ('wielorodzinna', 'Zabudowa wielorodzinna'),
    ]

    adres_nieruchomosci = models.CharField(max_length=255)
    liczba_mieszkancow = models.PositiveIntegerField()
    typ_zabudowy = models.CharField(max_length=20, choices=TYP_ZABUDOWY_CHOICES)
    posiada_kompostownik = models.BooleanField(default=False)
    obliczona_oplata = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # Pola 'status', 'wnioskodawca' i 'data_zlozenia' są dziedziczone z Wniosek

    class Meta:
        verbose_name = "Deklaracja śmieciowa"
        verbose_name_plural = "Deklaracje śmieciowe"

    def __str__(self):
        return f"Deklaracja dla {self.adres_nieruchomosci}"

    def get_absolute_url(self):
        return reverse('ogolne:wniosek_detail', kwargs={'pk': self.pk})