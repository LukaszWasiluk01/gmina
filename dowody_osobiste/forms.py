from django import forms
from .models import WniosekDowod

class WniosekDowodForm(forms.ModelForm):
    """
    Formularz dla użytkownika do składania wniosku o dowód.
    """
    class Meta:
        model = WniosekDowod
        fields = ['powod_wydania', 'inny_powod_wydania', 'zdjecie']
        labels = {
            'powod_wydania': 'Proszę wybrać powód ubiegania się o nowy dowód',
            'zdjecie': 'Proszę załączyć aktualne zdjęcie',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['zdjecie'].required = True

    def clean(self):
        """
        Niestandardowa walidacja formularza.
        """
        cleaned_data = super().clean()
        powod_wydania = cleaned_data.get("powod_wydania")
        inny_powod_wydania = cleaned_data.get("inny_powod_wydania")

        if powod_wydania == 'inny' and not inny_powod_wydania:
            self.add_error('inny_powod_wydania', 'To pole jest wymagane, jeśli wybrano powód "Inny".')

        if powod_wydania != 'inny' and inny_powod_wydania:
            cleaned_data['inny_powod_wydania'] = ''

        return cleaned_data

class RozpatrzWniosekDowodForm(forms.ModelForm):
    """
    Formularz dla urzędnika. Służy tylko do wpisania uzasadnienia.
    """
    class Meta:
        model = WniosekDowod
        fields = ["uzasadnienie_odrzucenia"]
        widgets = {
            "uzasadnienie_odrzucenia": forms.Textarea(attrs={"rows": 4, "placeholder": "Wpisz uzasadnienie tylko w przypadku odrzucenia wniosku..."}),
        }
        labels = {
            "uzasadnienie_odrzucenia": "Uzasadnienie decyzji (opcjonalne)"
        }