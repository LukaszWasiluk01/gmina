# lukaszwasiluk01/gmina/gmina-master/podatki/models.py

from django.db import models
from ogolne.models import Mieszkaniec  # Decyzje i wpłaty są powiązane z mieszkańcami

class DecyzjaPodatkowa(models.Model):
    mieszkaniec = models.ForeignKey(Mieszkaniec, on_delete=models.CASCADE, related_name='decyzje_podatkowe')
    rok_podatkowy = models.PositiveIntegerField()
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    termin_platnosci = models.DateField()
    czy_oplacona = models.BooleanField(default=False)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Decyzja podatkowa"
        verbose_name_plural = "Decyzje podatkowe"
        ordering = ['-rok_podatkowy', '-termin_platnosci']

    def __str__(self):
        return f"Decyzja dla {self.mieszkaniec} na rok {self.rok_podatkowy}"

class Wplata(models.Model):
    decyzja = models.ForeignKey(DecyzjaPodatkowa, on_delete=models.CASCADE, related_name='wplaty')
    kwota_wplaty = models.DecimalField(max_digits=10, decimal_places=2)
    data_wplaty = models.DateField(auto_now_add=True)
    urzednik_rejestrujacy = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'groups__name': 'Urzędnik ds. podatków'}
    )

    class Meta:
        verbose_name = "Wpłata"
        verbose_name_plural = "Wpłaty"

    def __str__(self):
        return f"Wpłata {self.kwota_wplaty} PLN dla decyzji {self.decyzja.id}"