# dotacje/forms.py

from django import forms
from .models import WniosekDotacja

class WniosekDotacjaForm(forms.ModelForm):
    class Meta:
        model = WniosekDotacja
        fields = ['tytul_projektu', 'opis_projektu', 'wnioskowana_kwota']

class WeryfikacjaFormalnaForm(forms.ModelForm):
    """Formularz dla urzędnika ds. dotacji."""
    class Meta:
        model = WniosekDotacja
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[
                ('Do oceny komisji', 'Poprawny formalnie (przekaż do komisji)'),
                ('Braki formalne', 'Wezwij do uzupełnienia braków'),
                ('Odrzucony', 'Odrzuć (błędy nieusuwalne)'),
            ])
        }

class OcenaKomisjiForm(forms.ModelForm):
    """Formularz dla komisji."""
    class Meta:
        model = WniosekDotacja
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[
                ('Do decyzji wójta', 'Rekomendacja pozytywna (przekaż do wójta)'),
                ('Odrzucony', 'Rekomendacja negatywna (odrzuć)'),
            ])
        }

class DecyzjaWojtaForm(forms.ModelForm):
    """Formularz dla wójta."""
    class Meta:
        model = WniosekDotacja
        fields = ['status', 'kwota_przyznana'] # Wójt może też ustalić finalną kwotę
        widgets = {
            'status': forms.Select(choices=[
                ('Zatwierdzony', 'Zatwierdź dotację'),
                ('Odrzucony', 'Odrzuć dotację'),
            ])
        }

class RealizacjaSkarbnikaForm(forms.ModelForm):
    """Formularz dla skarbnika."""
    class Meta:
        model = WniosekDotacja
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[
                ('Zrealizowany', 'Potwierdź wypłatę dotacji'),
            ])
        }