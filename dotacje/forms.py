# gmina/dotacje/forms.py

from django import forms
from .models import WniosekDotacja

class WniosekDotacjaForm(forms.ModelForm):
    """Formularz dla wnioskodawcy do składania wniosku o dotację."""
    class Meta:
        model = WniosekDotacja
        # Pola, które wypełnia wnioskodawca
        fields = ['tytul_projektu', 'opis_projektu', 'wnioskowana_kwota']
        widgets = {
            'opis_projektu': forms.Textarea(attrs={'rows': 5}),
        }

class WeryfikacjaKomisjiForm(forms.ModelForm):
    """Formularz dla komisji ds. dotacji."""
    class Meta:
        model = WniosekDotacja
        # Komisja zmienia tylko status
        fields = ['status']
        # Ograniczenie wyboru tylko do możliwych decyzji komisji
        widgets = {
            'status': forms.Select(choices=[
                ('W weryfikacji komisji', 'Przekaż do wójta (rekomendacja pozytywna)'),
                ('Odrzucony', 'Odrzuć wniosek')
            ])
        }

class RekomendacjaWojtaForm(forms.ModelForm):
    """Formularz dla wójta."""
    class Meta:
        model = WniosekDotacja
        fields = ['status']
        # Ograniczenie wyboru tylko do możliwych decyzji wójta
        widgets = {
            'status': forms.Select(choices=[
                ('Zatwierdzony', 'Zatwierdź dotację'),
                ('Odrzucony', 'Odrzuć dotację')
            ])
        }

class PrzelewDotacjiForm(forms.ModelForm):
    """Formularz dla urzędnika do oznaczenia przelewu."""
    class Meta:
        model = WniosekDotacja
        fields = ['status']
        # Urzędnik może tylko potwierdzić realizację
        widgets = {
            'status': forms.Select(choices=[
                ('Zrealizowany', 'Potwierdź realizację (przelew wykonany)'),
            ])
        }