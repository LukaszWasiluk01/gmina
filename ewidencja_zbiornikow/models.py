# ewidencja_zbiornikow/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek, Adres

class DeklaracjaZbiornika(Wniosek):
    adres_nieruchomosci = models.ForeignKey(Adres, on_delete=models.CASCADE)
    pojemnosc_zbiornika = models.DecimalField(max_digits=6, decimal_places=2, help_text="Pojemność w m³")

    class Meta:
        verbose_name = "Deklaracja posiadania zbiornika"
        verbose_name_plural = "Deklaracje posiadania zbiorników"

    def __str__(self):
        return f"Deklaracja zbiornika {self.id} dla adresu {self.adres_nieruchomosci}"

    def get_absolute_url(self):
        # Ta deklaracja nie ma dedykowanego widoku szczegółów, więc kieruje do listy ogólnej
        return reverse('ogolne:moje_wnioski')

class DeklaracjaOproznienia(Wniosek):
    deklaracja_zbiornika = models.ForeignKey(DeklaracjaZbiornika, on_delete=models.CASCADE)
    data_oproznienia = models.DateField()
    ilosc_sciekow = models.DecimalField(max_digits=6, decimal_places=2, help_text="Ilość w m³")

    class Meta:
        verbose_name = "Deklaracja opróżnienia zbiornika"
        verbose_name_plural = "Deklaracje opróżnienia zbiorników"

    def __str__(self):
        return f"Deklaracja opróżnienia {self.id} dla zbiornika {self.deklaracja_zbiornika.id}"

    def get_absolute_url(self):
        # Ta deklaracja również nie ma dedykowanego widoku szczegółów
        return reverse('ogolne:moje_wnioski')