from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Adres, Mieszkaniec


class RejestracjaForm(UserCreationForm):
    first_name = forms.CharField(label="Imię", max_length=30, required=True)
    last_name = forms.CharField(label="Nazwisko", max_length=30, required=True)
    email = forms.EmailField(label="Email", required=True)
    pesel = forms.CharField(label="PESEL", max_length=11, required=True)

    PLEC_CHOICES = [
        ("M", "Mężczyzna"),
        ("K", "Kobieta"),
    ]
    plec = forms.ChoiceField(
        label="Płeć",
        choices=PLEC_CHOICES,
        widget=forms.Select,
        initial="M",
        required=True,
    )

    ulica = forms.CharField(label="Ulica", max_length=100)
    numer_domu = forms.CharField(label="Numer domu", max_length=10)
    kod_pocztowy = forms.CharField(label="Kod pocztowy", max_length=10)
    miejscowosc = forms.CharField(label="Miejscowość", max_length=100)
    data_urodzenia = forms.DateField(
        label="Data urodzenia", widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "pesel",
            "plec",
            "ulica",
            "numer_domu",
            "kod_pocztowy",
            "miejscowosc",
            "data_urodzenia",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            if not Mieszkaniec.objects.filter(user=user).exists():
                adres, _ = Adres.objects.get_or_create(
                    ulica=self.cleaned_data["ulica"],
                    numer_domu=self.cleaned_data["numer_domu"],
                    kod_pocztowy=self.cleaned_data["kod_pocztowy"],
                    miejscowosc=self.cleaned_data["miejscowosc"],
                )

                mieszkaniec = Mieszkaniec.objects.create(
                    user=user,
                    imie=self.cleaned_data["first_name"],
                    nazwisko=self.cleaned_data["last_name"],
                    pesel=self.cleaned_data["pesel"],
                    plec=self.cleaned_data["plec"],
                    data_urodzenia=self.cleaned_data["data_urodzenia"],
                    adres=adres,
                )
                mieszkaniec.save()
        return user
