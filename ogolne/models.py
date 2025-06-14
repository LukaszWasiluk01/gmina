# gmina/ogolne/models.py

from django.db import models
from django.conf import settings # Lepsza praktyka niż importowanie User bezpośrednio

class Wniosek(models.Model):
    """
    Abstrakcyjny model bazowy dla wszystkich wniosków i deklaracji w systemie.
    """
    # Domyślne statusy, mogą być nadpisane w modelach dziedziczących
    STATUS_CHOICES = [
        ('Złożony', 'Złożony'),
        ('Zaakceptowany', 'Zaakceptowany'),
        ('Odrzucony', 'Odrzucony'),
    ]

    # Wspólne pola dla wszystkich wniosków
    wnioskodawca = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Złożony')
    data_zlozenia = models.DateTimeField(auto_now_add=True)
    powod_odrzucenia = models.TextField(blank=True, null=True, verbose_name="Powód odrzucenia (opcjonalnie)")

    class Meta:
        abstract = True
        ordering = ['-data_zlozenia'] # Sortowanie od najnowszych

    def __str__(self):
        return f"Wniosek nr {self.pk} od {self.wnioskodawca.username}"


class Adres(models.Model):
    ulica = models.CharField(max_length=100)
    numer_domu = models.CharField(max_length=10)
    kod_pocztowy = models.CharField(max_length=10)
    miejscowosc = models.CharField(max_length=100)


class Mieszkaniec(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    pesel = models.CharField(max_length=11, unique=True)
    data_urodzenia = models.DateField(null=False, blank=False)
    data_zgonu = models.DateField(null=True, blank=True)

    PLEC_CHOICES = [
        ("M", "Mężczyzna"),
        ("K", "Kobieta"),
    ]

    plec = models.CharField(
        max_length=1, choices=PLEC_CHOICES, verbose_name="Płeć", default="M"
    )

    ojciec = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="dzieci_jako_ojciec",
    )
    matka = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="dzieci_jako_matka",
    )

    partner = models.OneToOneField(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="partner_reverse",
    )

    adres = models.ForeignKey(
        Adres,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="mieszkancy",
    )

    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.pesel})"
