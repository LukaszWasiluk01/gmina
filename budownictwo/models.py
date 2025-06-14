# gmina/budownictwo/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek

class Adres(models.Model):
    ulica = models.CharField(max_length=100)
    numer_domu = models.CharField(max_length=10)
    numer_mieszkania = models.CharField(max_length=10, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=6)
    miejscowosc = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ulica} {self.numer_domu}, {self.miejscowosc}"

class WniosekBudowlany(Wniosek):
    # Nadpisujemy statusy na te specyficzne dla budownictwa
    STATUS_CHOICES = [
        ('Złożony', 'Złożony'),
        ('Zweryfikowany', 'Zweryfikowany przez urzędnika'),
        ('Zatwierdzony', 'Zatwierdzony przez inspektora'),
        ('Odrzucony', 'Odrzucony'),
    ]

    adres_inwestycji = models.ForeignKey(Adres, on_delete=models.CASCADE)
    rodzaj_inwestycji = models.CharField(max_length=255)

    # Pole status jest teraz dziedziczone, więc je nadpisujemy, a nie tworzymy od nowa
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Złożony')

    def __str__(self):
        return f"Wniosek budowlany: {self.rodzaj_inwestycji}"

    def get_absolute_url(self):
        return reverse('ogolne:wniosek_detail', kwargs={'pk': self.pk})