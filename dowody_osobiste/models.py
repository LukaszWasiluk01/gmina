from django.db import models
from django.urls import reverse

from ogolne.models import Wniosek

class WniosekDowod(Wniosek):
    """
    Model reprezentujący wniosek o wydanie dowodu osobistego.
    """
    STATUS_CHOICES = [
        ("Złożony", "Złożony"),
        ("Przekazany do PWPW", "Przekazany do realizacji (PWPW)"),
        ("Gotowy do odbioru", "Gotowy do odbioru w urzędzie"),
        ("Odebrany", "Odebrany przez wnioskodawcę"),
        ("Odrzucony", "Odrzucony"),
    ]

    POWOD_WYDANIA_CHOICES = [
        ('pierwszy_dowod', 'Pierwszy dowód osobisty'),
        ('utrata_dowodu', 'Utrata lub uszkodzenie dowodu'),
        ('zmiana_danych', 'Zmiana danych zawartych w dowodzie'),
        ('zmiana_wizerunku', 'Zmiana wizerunku twarzy'),
        ('uplyw_waznosci', 'Upływ terminu ważności dowodu'),
        ('uszkodzenie_dowodu', 'Uszkodzenie dowodu'),
        ('inny', 'Inny powód'),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Złożony")

    powod_wydania = models.CharField(max_length=50, choices=POWOD_WYDANIA_CHOICES)

    inny_powod_wydania = models.CharField(max_length=255, blank=True, null=True, verbose_name="Inny powód (proszę opisać)")

    zdjecie = models.ImageField(upload_to='zdjecia_dowodowe/')

    class Meta:
        verbose_name = "Wniosek o dowód osobisty"
        verbose_name_plural = "Wnioski o dowód osobisty"
        ordering = ['-data_zlozenia']

    def __str__(self):
        return f"Wniosek o dowód dla {self.wnioskodawca.username}"

    def get_absolute_url(self):
        """
        ZMIANA: Wskazuje na nowy, uniwersalny widok szczegółów.
        """
        return reverse("dowody_osobiste:wniosek_detail", kwargs={"pk": self.pk})