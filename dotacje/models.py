from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class WniosekDotacja(models.Model):
    STATUS = [
        ("oczekuje", "Oczekuje"),
        ("zaakceptowany_komisja", "Zaakceptowany przez komisję"),
        ("odrzucony_komisja", "Odrzucony przez komisję"),
        ("zatwierdzony_wojt", "Zatwierdzony przez wójta"),
        ("odrzucony_wojt", "Odrzucony przez wójta"),
        ("zrealizowany", "Zrealizowany"),
    ]

    wnioskodawca = models.ForeignKey(User, on_delete=models.CASCADE)
    tytul = models.CharField(max_length=200)
    opis = models.TextField()
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS, default="oczekuje")

    def __str__(self):
        return f"{self.tytul} - {self.status}"
