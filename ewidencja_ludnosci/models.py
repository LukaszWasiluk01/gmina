from django.db import models

# Create your models here.


class StatystykaLudnosci(models.Model):
    data = models.DateField(auto_now_add=True)
    liczba_mieszkancow = models.PositiveIntegerField()
    liczba_dzieci = models.PositiveIntegerField()
    liczba_seniorow = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Statystyka ludności"
        verbose_name_plural = "Statystyki ludności"
