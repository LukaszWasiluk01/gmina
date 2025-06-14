# gmina/budownictwo/forms.py

from django import forms
from .models import WniosekBudowlany, Adres

class AdresForm(forms.ModelForm):
    class Meta:
        model = Adres
        fields = '__all__'

class WniosekBudowlanyForm(forms.ModelForm):
    """Formularz do składania wniosku o pozwolenie na budowę."""
    class Meta:
        model = WniosekBudowlany
        # Użytkownik podaje tylko te dane. Reszta jest dziedziczona lub ustawiana automatycznie.
        fields = ['rodzaj_inwestycji']

class WeryfikujWniosekBudowlanyForm(forms.ModelForm):
    """Formularz dla urzędnika budowlanego."""
    class Meta:
        model = WniosekBudowlany
        fields = ['status', 'powod_odrzucenia']
        widgets = {
            'status': forms.Select(choices=[
                ('Zweryfikowany', 'Zweryfikuj i przekaż do inspektora'),
                ('Odrzucony', 'Odrzuć wniosek')
            ]),
            'powod_odrzucenia': forms.Textarea(attrs={'rows': 3}),
        }

class DecyzjaInspektoraForm(forms.ModelForm):
    """Formularz dla inspektora nadzoru budowlanego."""
    class Meta:
        model = WniosekBudowlany
        fields = ['status', 'powod_odrzucenia']
        widgets = {
            'status': forms.Select(choices=[
                ('Zatwierdzony', 'Zatwierdź wniosek (wydaj pozwolenie)'),
                ('Odrzucony', 'Odrzuć wniosek')
            ]),
            'powod_odrzucenia': forms.Textarea(attrs={'rows': 3}),
        }