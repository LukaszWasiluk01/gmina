from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class WniosekRejestracjaSamochodu(models.Model):
    STATUSY = [
        ("oczekuje", "Oczekuje"),
        ("zatwierdzony", "Zatwierdzony"),
        ("odrzucony", "Odrzucony"),
    ]

    wnioskodawca = models.ForeignKey(User, on_delete=models.CASCADE)
    marka = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    numer_rejestracyjny = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUSY, default="oczekuje")
    data_zlozenia = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Wniosek o rejestrację samochodu"
        verbose_name_plural = "Wnioski o rejestrację samochodu"

    def __str__(self):
        return f"{self.marka} {self.model} - {self.numer_rejestracyjny}"
