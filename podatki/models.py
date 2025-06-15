from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class DecyzjaPodatkowa(models.Model):
    podatnik = models.ForeignKey(User, on_delete=models.CASCADE)
    rok_podatkowy = models.PositiveIntegerField()
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    termin_platnosci = models.DateField()
    oplacona = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Decyzja podatkowa"
        verbose_name_plural = "Decyzje podatkowe"

    def __str__(self):
        return f"Decyzja podatkowa dla {self.podatnik.username} na rok {self.rok_podatkowy}"

    def get_absolute_url(self):

        return reverse("podatki:rejestruj_wplate", kwargs={"pk": self.pk})


class Wplata(models.Model):
    decyzja = models.ForeignKey(
        DecyzjaPodatkowa, on_delete=models.CASCADE, related_name="wplaty"
    )
    data_wplaty = models.DateField(auto_now_add=True)
    kwota_wplaty = models.DecimalField(max_digits=10, decimal_places=2)
    urzednik = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Wpłata"
        verbose_name_plural = "Wpłaty"

    def __str__(self):
        return f"Wpłata {self.kwota_wplaty} zł do decyzji {self.decyzja.id}"
