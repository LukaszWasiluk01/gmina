# lukaszwasiluk01/gmina/gmina-master/ewidencja_zbiornikow/models.py

from django.db import models
from django.urls import reverse
from ogolne.models import Wniosek  # Import bazowego modelu Wniosek

# Model dla deklaracji posiadanych zbiorników
class DeklaracjaZbiornika(Wniosek):
    STATUS_CHOICES = [
        ('Złożona', 'Złożona'),
        ('Zaakceptowana', 'Zaakceptowana'),
    ]

    adres_nieruchomosci = models.CharField(max_length=255)
    pojemnosc_zbiornika = models.DecimalField(max_digits=10, decimal_places=2, help_text="Pojemność w m³")

    class Meta:
        verbose_name = "Deklaracja o posiadanym zbiorniku"
        verbose_name_plural = "Deklaracje o posiadanych zbiornikach"

    def __str__(self):
        return f"Deklaracja zbiornika dla {self.adres_nieruchomosci}"

    def get_absolute_url(self):
        return reverse('ogolne:wniosek_detail', kwargs={'pk': self.pk})

# Model dla deklaracji opróżnienia zbiornika
class DeklaracjaOproznienia(Wniosek):
    STATUS_CHOICES = [
        ('Złożona', 'Złożona'),
        ('Zaakceptowana', 'Zaakceptowana'),
    ]

    # Powiązanie zadeklarowanego zbiornika, jeśli istnieje
    zbiornik = models.ForeignKey(DeklaracjaZbiornika, on_delete=models.CASCADE, null=True, blank=True)
    data_oproznienia = models.DateField()
    ilosc_opadu = models.DecimalField(max_digits=10, decimal_places=2, help_text="Ilość w m³")

    class Meta:
        verbose_name = "Deklaracja opróżnienia zbiornika"
        verbose_name_plural = "Deklaracje opróżnienia zbiorników"

    def __str__(self):
        return f"Opróżnienie zbiornika z dnia {self.data_oproznienia}"

    def get_absolute_url(self):
        return reverse('ogolne:wniosek_detail', kwargs={'pk': self.pk})