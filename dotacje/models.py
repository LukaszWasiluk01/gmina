from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

from ogolne.models import Wniosek

class WniosekDotacja(Wniosek):

    STATUS_CHOICES = [
        ("Złożony", "Złożony"),
        ("Do oceny komisji", "Przekazany do oceny komisji"),
        ("Do decyzji wójta", "Oczekuje na decyzję wójta"),
        ("Zatwierdzony", "Zatwierdzony przez wójta"),
        ("Do realizacji (Skarbnik)", "Oczekuje na przelew skarbnika"),
        ("Zrealizowany", "Dotacja wypłacona"),
        ("Odrzucony", "Odrzucony"),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Złożony")

    tytul_projektu = models.CharField(max_length=255)
    opis_projektu = models.TextField()
    wnioskowana_kwota = models.DecimalField(max_digits=10, decimal_places=2)
    kwota_przyznana = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    numer_konta_bankowego = models.CharField(
        max_length=26,
        validators=[RegexValidator(r'^\d{26}$', 'Numer konta musi składać się z 26 cyfr.')],
        help_text="Proszę podać 26-cyfrowy numer konta bankowego (bez spacji i myślników)."
    )

    class Meta:
        verbose_name = "Wniosek o dotację"
        verbose_name_plural = "Wnioski o dotacje"
        ordering = ['-data_zlozenia']

    def __str__(self):
        return f'Wniosek o dotację: "{self.tytul_projektu}"'

    def get_absolute_url(self):
        return reverse("dotacje:wniosek_detail", kwargs={"pk": self.pk})