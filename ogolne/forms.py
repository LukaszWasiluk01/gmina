from django import forms
from django.contrib.auth.models import User

from .models import Mieszkaniec


class RejestracjaForm(forms.Form):

    username = forms.CharField(max_length=150, label="Nazwa użytkownika")
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Potwierdź hasło"
    )
    first_name = forms.CharField(max_length=30, label="Imię")
    last_name = forms.CharField(max_length=150, label="Nazwisko")
    email = forms.EmailField(label="Adres e-mail")

    pesel = forms.CharField(max_length=11, label="PESEL")
    data_urodzenia = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Data urodzenia"
    )
    plec = forms.ChoiceField(choices=Mieszkaniec.PLEC_CHOICES, label="Płeć")

    ulica = forms.CharField(max_length=100, label="Ulica")
    numer_domu = forms.CharField(max_length=10, label="Numer domu")
    numer_mieszkania = forms.CharField(
        max_length=10, required=False, label="Numer mieszkania"
    )
    kod_pocztowy = forms.CharField(max_length=6, label="Kod pocztowy")
    miejscowosc = forms.CharField(max_length=100, label="Miejscowość")

    def clean_username(self):
        """Sprawdza, czy nazwa użytkownika jest już zajęta."""
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ta nazwa użytkownika jest już zajęta.")
        return username

    def clean_email(self):
        """Sprawdza, czy email jest już używany."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten adres e-mail jest już używany.")
        return email

    def clean_pesel(self):
        """Sprawdza, czy PESEL jest już w bazie."""
        pesel = self.cleaned_data.get("pesel")
        if Mieszkaniec.objects.filter(pesel=pesel).exists():
            raise forms.ValidationError("Ten numer PESEL jest już zarejestrowany.")
        return pesel

    def clean(self):
        """Sprawdza, czy hasła się zgadzają."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Hasła nie są identyczne.")
        return cleaned_data
