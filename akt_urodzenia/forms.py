from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from ogolne.models import Mieszkaniec


class ZgloszenieUrodzeniaForm(forms.Form):
    imie = forms.CharField(label="Imię", max_length=50)
    nazwisko = forms.CharField(label="Nazwisko", max_length=50)
    pesel_rodzica = forms.CharField(
        label="PESEL drugiego rodzica", max_length=11, min_length=11
    )
    PLEC_CHOICES = [
        ("M", "Mężczyzna"),
        ("K", "Kobieta"),
    ]

    plec = forms.ChoiceField(
        label="Płeć dziecka",
        choices=PLEC_CHOICES,
    )
    data_urodzenia = forms.DateField(
        label="Data urodzenia", widget=forms.DateInput(attrs={"type": "date"})
    )

    def clean_pesel_rodzica(self):
        pesel = self.cleaned_data["pesel_rodzica"]
        if not Mieszkaniec.objects.filter(pesel=pesel).exists():
            raise ValidationError("Nie znaleziono mieszkańca o podanym numerze PESEL.")
        return pesel

    def clean_data_urodzenia(self):
        data = self.cleaned_data["data_urodzenia"]
        if data > timezone.now().date():
            raise ValidationError("Data urodzenia nie może być z przyszłości.")
        return data
