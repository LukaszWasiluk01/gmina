from django import forms

from .models import WniosekBudowlany


class WniosekBudowlanyForm(forms.ModelForm):

    ulica = forms.CharField(max_length=100)
    numer_domu = forms.CharField(max_length=10)
    numer_mieszkania = forms.CharField(max_length=10, required=False)
    kod_pocztowy = forms.CharField(max_length=6)
    miejscowosc = forms.CharField(max_length=100)

    class Meta:
        model = WniosekBudowlany

        fields = [
            "tytul",
            "opis_budowy",
            "rodzaj_inwestycji",
            "numer_dzialki",
            "ulica",
            "numer_domu",
            "numer_mieszkania",
            "kod_pocztowy",
            "miejscowosc",
        ]


class RozpatrzWniosekForm(forms.ModelForm):
    class Meta:
        model = WniosekBudowlany
        fields = ["status", "uzasadnienie_odrzucenia"]
        widgets = {
            "uzasadnienie_odrzucenia": forms.Textarea(attrs={"rows": 3}),
        }


class DecyzjaInspektoraForm(forms.ModelForm):
    class Meta:
        model = WniosekBudowlany
        fields = ["status", "uzasadnienie_odrzucenia"]
