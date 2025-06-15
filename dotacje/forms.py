from django import forms
from .models import WniosekDotacja

class WniosekDotacjaForm(forms.ModelForm):
    """
    Formularz dla użytkownika do składania wniosku.
    ZMIANA: Dodano pole `numer_konta_bankowego`.
    """
    class Meta:
        model = WniosekDotacja
        fields = ["tytul_projektu", "opis_projektu", "wnioskowana_kwota", "numer_konta_bankowego"]
        labels = {
            "numer_konta_bankowego": "Numer konta bankowego do wypłaty dotacji"
        }

class RozpatrzWniosekDotacjaForm(forms.ModelForm):
    """
    JEDEN, UNIWERSALNY FORMULARZ DLA WSZYSTKICH URZĘDNIKÓW.
    Służy do wpisania uzasadnienia lub kwoty przyznanej przez wójta.
    """
    class Meta:
        model = WniosekDotacja
        fields = ["kwota_przyznana", "uzasadnienie_odrzucenia"]
        widgets = {
            "uzasadnienie_odrzucenia": forms.Textarea(attrs={"rows": 4, "placeholder": "Wpisz uzasadnienie, jeśli odrzucasz wniosek lub chcesz dodać komentarz..."}),
        }
        labels = {
            "kwota_przyznana": "Kwota przyznanej dotacji (PLN)",
            "uzasadnienie_odrzucenia": "Uzasadnienie / Komentarz (opcjonalne)"
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)
        status = kwargs.pop('status', None)
        super().__init__(*args, **kwargs)

        if not (user and user.groups.filter(name="Wójt").exists() and status == "Do decyzji wójta"):
            self.fields.pop('kwota_przyznana')