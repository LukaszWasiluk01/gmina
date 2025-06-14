# gmina/akt_urodzenia/forms.py

from django import forms
from .models import ZgloszenieUrodzenia
from ogolne.models import Mieszkaniec

class ZgloszenieUrodzeniaForm(forms.ModelForm):
    """Formularz do zgłaszania urodzenia przez wnioskodawcę."""
    class Meta:
        model = ZgloszenieUrodzenia
        # Wykluczamy pola ustawiane automatycznie przez system
        exclude = ['wnioskodawca', 'status', 'powod_odrzucenia', 'nowy_mieszkaniec']

class RozpatrzZgloszenieForm(forms.ModelForm):
    """Formularz dla urzędnika do akceptacji lub odrzucenia zgłoszenia."""
    class Meta:
        model = ZgloszenieUrodzenia
        # Urzędnik może zmienić tylko status i ewentualnie podać powód odrzucenia
        fields = ['status', 'powod_odrzucenia']
        widgets = {
            'status': forms.Select(choices=[
                ('Zaakceptowany', 'Zaakceptuj zgłoszenie'),
                ('Odrzucony', 'Odrzuć zgłoszenie')
            ]),
            'powod_odrzucenia': forms.Textarea(attrs={'rows': 3}),
        }