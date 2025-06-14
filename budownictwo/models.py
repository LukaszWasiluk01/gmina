from django.db import models
from django.urls import reverse

from ogolne.models import Adres, Wniosek


class WniosekBudowlany(Wniosek):

    adres_inwestycji = models.ForeignKey(Adres, on_delete=models.CASCADE)
    rodzaj_inwestycji = models.CharField(max_length=200)
    numer_dzialki = models.CharField(max_length=50)

    tytul = models.CharField(max_length=255, default="Wniosek o pozwolenie na budowę")
    opis_budowy = models.TextField()

    class Meta:
        verbose_name = "Wniosek budowlany"
        verbose_name_plural = "Wnioski budowlane"

    def __str__(self):
        return f"Wniosek budowlany nr {self.id} dla działki {self.numer_dzialki}"

    def get_absolute_url(self):

        return reverse("budownictwo:rozpatrz_wniosek", kwargs={"pk": self.pk})
