from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class DecyzjaPodatkowa(models.Model):
    """
    Model reprezentujący decyzję podatkową wystawioną dla użytkownika.
    """
    podatnik = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decyzje_podatkowe')
    rok_podatkowy = models.PositiveIntegerField()
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    termin_platnosci = models.DateField()
    data_wystawienia = models.DateTimeField(auto_now_add=True)
    oplacona = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Decyzja podatkowa"
        verbose_name_plural = "Decyzje podatkowe"
        ordering = ['-data_wystawienia']

        unique_together = ('podatnik', 'rok_podatkowy')

    def __str__(self):
        return f"Decyzja podatkowa dla {self.podatnik.username} na rok {self.rok_podatkowy}"

    def get_absolute_url(self):
        """
        ZMIANA: Wskazuje na nowy, uniwersalny widok szczegółów.
        """
        return reverse("podatki:decyzja_detail", kwargs={"pk": self.pk})

    @property
    def is_overdue(self):
        """Sprawdza, czy termin płatności minął i decyzja nie jest opłacona."""
        return self.termin_platnosci < timezone.now().date() and not self.oplacona

class Wplata(models.Model):
    """
    Model reprezentujący wpłatę dokonaną w ramach decyzji podatkowej.
    """
    decyzja = models.ForeignKey(DecyzjaPodatkowa, on_delete=models.CASCADE, related_name='wplaty')
    kwota_wplaty = models.DecimalField(max_digits=10, decimal_places=2)
    data_wplaty = models.DateTimeField(auto_now_add=True)

    urzednik = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='zarejestrowane_wplaty')

    class Meta:
        verbose_name = "Wpłata"
        verbose_name_plural = "Wpłaty"

    def __str__(self):
        return f"Wpłata {self.kwota_wplaty} zł do decyzji {self.decyzja.id}"