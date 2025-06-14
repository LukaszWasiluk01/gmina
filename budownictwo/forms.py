from django import forms
from .models import WniosekBudowlany

class WniosekBudowlanyForm(forms.ModelForm):
    ulica = forms.CharField(label="Ulica", max_length=100)
    numer_domu = forms.CharField(label="Numer domu", max_length=10)
    kod_pocztowy = forms.CharField(label="Kod pocztowy", max_length=10)
    miejscowosc = forms.CharField(label="Miejscowość", max_length=100)

    class Meta:
        model = WniosekBudowlany
        fields = ['tytul', 'opis_budowy', 'ulica', 'numer_domu', 'kod_pocztowy', 'miejscowosc']
        widgets = {
            'tytul': forms.TextInput(attrs={'class': 'form-control'}),
            'opis_budowy': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['ulica', 'numer_domu', 'kod_pocztowy', 'miejscowosc']:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

from django import forms
from .models import WniosekBudowlany

class WeryfikujWniosekBudowlanyForm(forms.ModelForm):
    powod_odrzucenia = forms.CharField(
        label="Powód odrzucenia",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
    )

    class Meta:
        model = WniosekBudowlany
        fields = ['opis_budowy', 'powod_odrzucenia']
        widgets = {
            'opis_budowy': forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }


class DecyzjaInspektoraForm(forms.ModelForm):
    powod_odrzucenia = forms.CharField(
        label="Powód odrzucenia",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
    )

    class Meta:
        model = WniosekBudowlany
        fields = ['opis_budowy', 'powod_odrzucenia']
        widgets = {
            'opis_budowy': forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }



