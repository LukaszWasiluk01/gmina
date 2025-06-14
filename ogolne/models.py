# ogolne/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Wniosek(models.Model):
    STATUS_CHOICES = [
        ('Złożony', 'Złożony'),
        ('W weryfikacji', 'W weryfikacji'),
        ('Zaakceptowany', 'Zaakceptowany'),
        ('Odrzucony', 'Odrzucony'),
    ]
    wnioskodawca = models.ForeignKey(User, on_delete=models.CASCADE)
    data_zlozenia = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Złożony')
    uzasadnienie_odrzucenia = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Wniosek {self.id} od {self.wnioskodawca.username}"

    def get_absolute_url(self):
        raise NotImplementedError("Musisz zaimplementować get_absolute_url w modelu potomnym!")

class Adres(models.Model):
    ulica = models.CharField(max_length=100)
    numer_domu = models.CharField(max_length=10)
    numer_mieszkania = models.CharField(max_length=10, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=6)
    miejscowosc = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ulica} {self.numer_domu}, {self.miejscowosc}"

    class Meta:
        verbose_name_plural = "Adresy"

class Mieszkaniec(models.Model):
    PLEC_CHOICES = [
        ('M', 'Mężczyzna'),
        ('K', 'Kobieta'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    pesel = models.CharField(max_length=11, unique=True)
    data_urodzenia = models.DateField()
    plec = models.CharField(max_length=1, choices=PLEC_CHOICES)
    imie_ojca = models.CharField(max_length=50, blank=True)
    imie_matki = models.CharField(max_length=50, blank=True)
    adres_zamieszkania = models.ForeignKey(Adres, on_delete=models.SET_NULL, null=True, related_name='mieszkancy_zamieszkania')
    adres_zameldowania = models.ForeignKey(Adres, on_delete=models.SET_NULL, null=True, related_name='mieszkancy_zameldowania')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name_plural = "Mieszkańcy"