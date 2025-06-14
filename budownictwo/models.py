from django.db import models
from ogolne.models import Adres, Wniosek


class WniosekBudowlany(Wniosek):
    adres_dzialki = models.ForeignKey(Adres, on_delete=models.CASCADE)
    opis_budowy = models.TextField()

    STATUS = [
        ("oczekuje", "Oczekuje weryfikacji"),
        ("zweryfikowany", "Zweryfikowany przez urzędnika"),
        ("zatwierdzony", "Zatwierdzony przez inspektora"),
        ("odrzucony", "Odrzucony"),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default="oczekuje")

    def __str__(self):
        return f"{self.tytul} – {self.status}"
