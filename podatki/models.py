from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class DecyzjaPodatkowa(models.Model):
    podatnik = models.ForeignKey(User, on_delete=models.CASCADE)
    tytul = models.CharField(max_length=200)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data_wydania = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Decyzja podatkowa"
        verbose_name_plural = "Decyzje podatkowe"

    def __str__(self):
        return f"{self.tytul} - {self.podatnik.username}"


class Wplata(models.Model):
    decyzja = models.ForeignKey(DecyzjaPodatkowa, on_delete=models.CASCADE)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data_wplaty = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Wpłata"
        verbose_name_plural = "Wpłaty"
