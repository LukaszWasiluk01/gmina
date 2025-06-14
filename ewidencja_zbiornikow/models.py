from django.contrib.auth.models import User
from django.db import models

from ogolne.models import Wniosek

# Create your models here.


class DeklaracjaZbiornika(Wniosek):
    adres = models.CharField(max_length=200)
    pojemnosc_l = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Deklaracja zbiornika"
        verbose_name_plural = "Deklaracje zbiorników"


class DeklaracjaOproznienia(Wniosek):
    zbiornik = models.ForeignKey(DeklaracjaZbiornika, on_delete=models.CASCADE)
    data_oproznienia = models.DateField()

    class Meta:
        verbose_name = "Deklaracja opróżnienia"
        verbose_name_plural = "Deklaracje opróżnień"
