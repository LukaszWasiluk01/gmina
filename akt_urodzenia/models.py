from django.db import models

from ogolne.models import Mieszkaniec, Wniosek

# Create your models here.


class ZgloszenieUrodzenia(Wniosek):
    mieszkaniec = models.ForeignKey(Mieszkaniec, on_delete=models.CASCADE)
    data_urodzenia = models.DateTimeField()

    STATUS = [
        ("oczekuje", "Oczekuje"),
        ("zaakceptowane", "Zaakceptowane"),
        ("odrzucone", "Odrzucone"),
    ]

    status = models.CharField(max_length=13, choices=STATUS, default="oczekuje")
