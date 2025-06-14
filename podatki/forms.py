from django import forms

from .models import DecyzjaPodatkowa, Wplata


class DecyzjaPodatkowaForm(forms.ModelForm):
    class Meta:
        model = DecyzjaPodatkowa

        fields = ["podatnik", "rok_podatkowy", "kwota", "termin_platnosci"]


class WplataForm(forms.ModelForm):
    class Meta:
        model = Wplata
        fields = ["kwota_wplaty"]
