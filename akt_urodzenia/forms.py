from django import forms

from .models import ZgloszenieUrodzenia


class ZgloszenieUrodzeniaForm(forms.ModelForm):
    class Meta:
        model = ZgloszenieUrodzenia
        exclude = ["wnioskodawca", "status", "pesel_dziecka", "uzasadnienie_odrzucenia"]


class RozpatrzZgloszenieForm(forms.ModelForm):
    class Meta:
        model = ZgloszenieUrodzenia

        fields = ["status", "uzasadnienie_odrzucenia"]
