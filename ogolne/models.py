from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Wniosek(models.Model):
    wnioskodawca = models.ForeignKey(User, on_delete=models.CASCADE)
    tytul = models.CharField(max_length=200)
    data_zlozenia = models.DateTimeField(auto_now_add=True)
    powod_odrzucenia = models.TextField(blank=True)


    class Meta:
        abstract = True


class Adres(models.Model):
    ulica = models.CharField(max_length=100)
    numer_domu = models.CharField(max_length=10)
    kod_pocztowy = models.CharField(max_length=10)
    miejscowosc = models.CharField(max_length=100)


class Mieszkaniec(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
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
