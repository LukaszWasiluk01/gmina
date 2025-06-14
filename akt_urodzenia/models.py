# akt_urodzenia/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek

class ZgloszenieUrodzenia(Wniosek):
    imie_dziecka = models.CharField(max_length=50)
    nazwisko_dziecka = models.CharField(max_length=50)
    plec_dziecka = models.CharField(max_length=10, choices=[('M', 'Mężczyzna'), ('K', 'Kobieta')])
    data_urodzenia_dziecka = models.DateField()
    miejsce_urodzenia_dziecka = models.CharField(max_length=100)
    imie_matki = models.CharField(max_length=50)
    nazwisko_rodowe_matki = models.CharField(max_length=50)
    imie_ojca = models.CharField(max_length=50)
    nazwisko_ojca = models.CharField(max_length=50)
    pesel_dziecka = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        verbose_name = "Zgłoszenie urodzenia"
        verbose_name_plural = "Zgłoszenia urodzeń"

    def __str__(self):
        return f"Zgłoszenie urodzenia dla {self.imie_dziecka} {self.nazwisko_dziecka}"

    def get_absolute_url(self):
        return reverse('akt_urodzenia:zgloszenie_detail', kwargs={'pk': self.pk})