from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class DeklaracjaSmieciowa(models.Model):
    TYP_ZABUDOWY = [
        ("jednorodzinna", "Jednorodzinna"),
        ("wielorodzinna", "Wielorodzinna"),
    ]

    wnioskodawca = models.ForeignKey(User, on_delete=models.CASCADE)
    liczba_osob = models.PositiveIntegerField()
    typ_zabudowy = models.CharField(max_length=20, choices=TYP_ZABUDOWY)
    status = models.CharField(max_length=20, default="oczekuje")  # lub 'wyliczona'
    oplata = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    data_zlozenia = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.wnioskodawca.username} - {self.data_zlozenia}"
