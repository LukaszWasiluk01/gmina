# akt_urodzenia/forms.py

from django import forms
from .models import ZgloszenieUrodzenia

class ZgloszenieUrodzeniaForm(forms.ModelForm):
    class Meta:
        model = ZgloszenieUrodzenia
        exclude = ['wnioskodawca', 'status', 'pesel_dziecka', 'uzasadnienie_odrzucenia']


class RozpatrzZgloszenieForm(forms.ModelForm):
    class Meta:
        model = ZgloszenieUrodzenia
        # Zmieniono 'powod_odrzucenia' na poprawną nazwę 'uzasadnienie_odrzucenia'
        fields = ['status', 'uzasadnienie_odrzucenia']