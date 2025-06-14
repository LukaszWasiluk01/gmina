# budownictwo/forms.py

from django import forms
from .models import WniosekBudowlany
from ogolne.models import Adres

class WniosekBudowlanyForm(forms.ModelForm):
    # Dodajemy pola dla modelu Adres, aby móc je zapisać razem
    ulica = forms.CharField(max_length=100)
    numer_domu = forms.CharField(max_length=10)
    numer_mieszkania = forms.CharField(max_length=10, required=False)
    kod_pocztowy = forms.CharField(max_length=6)
    miejscowosc = forms.CharField(max_length=100)

    class Meta:
        model = WniosekBudowlany
        # Zaktualizowano pola formularza
        fields = ['tytul', 'opis_budowy', 'rodzaj_inwestycji', 'numer_dzialki', 'ulica', 'numer_domu', 'numer_mieszkania', 'kod_pocztowy', 'miejscowosc']

class RozpatrzWniosekForm(forms.ModelForm):
    class Meta:
        model = WniosekBudowlany
        fields = ['status', 'uzasadnienie_odrzucenia']
        widgets = {
            'uzasadnienie_odrzucenia': forms.Textarea(attrs={'rows': 3}),
        }

class DecyzjaInspektoraForm(forms.ModelForm):
    class Meta:
        model = WniosekBudowlany
        fields = ['status', 'uzasadnienie_odrzucenia']