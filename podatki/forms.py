# podatki/forms.py

from django import forms
from .models import DecyzjaPodatkowa, Wplata

class DecyzjaPodatkowaForm(forms.ModelForm):
    class Meta:
        model = DecyzjaPodatkowa
        # Zmieniono 'mieszkaniec' na 'podatnik', aby pasowało do modelu
        fields = ['podatnik', 'rok_podatkowy', 'kwota', 'termin_platnosci']

class WplataForm(forms.ModelForm):
    class Meta:
        model = Wplata
        fields = ['kwota_wplaty']