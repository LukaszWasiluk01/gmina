from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class WniosekDowodowy(models.Model):
    STATUS = [
        ("oczekuje", "Oczekuje"),
        ("rozpatrzony", "Rozpatrzony"),
        ("przekazany", "Przekazany do PWPW"),
    ]

    wnioskodawca = models.ForeignKey(User, on_delete=models.CASCADE)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    pesel = models.CharField(max_length=11)
    adres_zameldowania = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS, default="oczekuje")
    data_zlozenia = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nazwisko} {self.imie} – {self.status}"
