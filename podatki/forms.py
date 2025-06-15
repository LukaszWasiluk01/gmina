from django import forms
from django.contrib.auth.models import User
from .models import DecyzjaPodatkowa, Wplata

class DecyzjaPodatkowaForm(forms.ModelForm):
    """
    Formularz dla URZĘDNIKA do tworzenia nowej decyzji podatkowej.
    """

    podatnik = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=False),
        label="Podatnik (mieszkaniec)"
    )

    class Meta:
        model = DecyzjaPodatkowa
        fields = ['podatnik', 'rok_podatkowy', 'kwota', 'termin_platnosci']
        widgets = {
            'termin_platnosci': forms.DateInput(attrs={'type': 'date'}),
        }

class WplataForm(forms.ModelForm):
    """
    Formularz dla URZĘDNIKA do rejestrowania wpłaty.
    """
    class Meta:
        model = Wplata
        fields = ['kwota_wplaty']
        labels = {
            'kwota_wplaty': 'Rejestrowana kwota wpłaty (PLN)'
        }