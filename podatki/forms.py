# gmina/podatki/forms.py

from django import forms
from .models import DecyzjaPodatkowa, Wplata

class DecyzjaPodatkowaForm(forms.ModelForm):
    """Formularz dla urzędnika do generowania nowej decyzji podatkowej."""

    # Używamy DateInput, aby w przeglądarce pojawił się wygodny kalendarz
    termin_platnosci = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = DecyzjaPodatkowa
        # Urzędnik wypełnia te pola. Pole 'czy_oplacona' ma wartość domyślną.
        fields = ['mieszkaniec', 'rok_podatkowy', 'kwota', 'termin_platnosci']

class WplataForm(forms.ModelForm):
    """Formularz do rejestrowania wpłaty do istniejącej decyzji."""
    class Meta:
        model = Wplata
        # Urzędnik wybiera decyzję i podaje kwotę wpłaty.
        # Reszta pól jest ustawiana automatycznie.
        fields = ['decyzja', 'kwota_wplaty']