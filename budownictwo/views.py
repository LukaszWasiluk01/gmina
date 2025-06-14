import random # Nie używane w tym kodzie, ale zostawione, jeśli jest potrzebne gdzie indziej.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from ogolne.models import Adres # Model Adres jest potrzebny do zapisu wniosku.

from .forms import WniosekBudowlanyForm, WeryfikujWniosekBudowlanyForm, DecyzjaInspektoraForm
from .models import WniosekBudowlany


class WnioskodawcaMixin(UserPassesTestMixin):
    """Mixin sprawdzający, czy użytkownik należy do grupy 'Wnioskodawca'."""
    def test_func(self):
        return self.request.user.groups.filter(name="Wnioskodawca").exists()


class UrzednikBudowlanyMixin(UserPassesTestMixin):
    """Mixin sprawdzający, czy użytkownik należy do grupy 'Urzędnik ds. budownictwa'."""
    def test_func(self):
        return self.request.user.groups.filter(name="Urzędnik ds. budownictwa").exists()


class InspektorNadzoruMixin(UserPassesTestMixin):
    """Mixin sprawdzający, czy użytkownik należy do grupy 'Inspektor nadzoru budowlanego'."""
    def test_func(self):
        return self.request.user.groups.filter(name="Inspektor nadzoru budowlanego").exists()


class ZlozWniosekBudowlanyView(LoginRequiredMixin, WnioskodawcaMixin, View):
    """Widok odpowiedzialny za wyświetlanie i przetwarzanie formularza składania wniosku budowlanego."""
    def get(self, request):
        # Wyświetla pusty formularz wniosku budowlanego
        form = WniosekBudowlanyForm()
        return render(request, "budownictwo/zloz_wniosek_budowlany.html", {"form": form})

    def post(self, request):
        # Tworzy instancję formularza z danymi przesłanymi przez użytkownika
        form = WniosekBudowlanyForm(request.POST)

        # Jeśli użytkownik kliknął przycisk "Zmień" na stronie potwierdzenia
        if request.POST.get("zmien"):
            # Ponownie renderuje formularz z wprowadzonymi danymi (do edycji)
            return render(request, "budownictwo/zloz_wniosek_budowlany.html", {"form": form})

        # Jeśli formularz jest prawidłowy
        if form.is_valid():
            # Renderuje stronę potwierdzenia, przekazując obiekt formularza z danymi
            return render(
                request,
                "budownictwo/potwierdz_wniosek_budowlany.html",
                {"form": form},
            )
        # Jeśli formularz nie jest prawidłowy, ponownie renderuje formularz z błędami walidacji
        return render(request, "budownictwo/zloz_wniosek_budowlany.html", {"form": form})


class PotwierdzWniosekBudowlanyView(LoginRequiredMixin, WnioskodawcaMixin, View):
    """Widok odpowiedzialny za potwierdzenie i zapisanie wniosku budowlanego."""
    def get(self, request):
        # Bezpośrednie wejście na tę stronę (GET) powinno przekierować do formularza składania wniosku.
        return redirect("budownictwo:zloz_wniosek_budowlany")

    def post(self, request):
        # Ponownie tworzy instancję formularza z danymi przesłanymi z ukrytych pól na stronie potwierdzenia
        form = WniosekBudowlanyForm(request.POST)

        # Sprawdza, czy dane z ukrytych pól są nadal prawidłowe
        if not form.is_valid():
            # Jeśli nie są, przekierowuje z powrotem do formularza składania wniosku z błędami
            # (może się to zdarzyć, jeśli użytkownik manipulował ukrytymi polami)
            return render(request, "budownictwo/zloz_wniosek_budowlany.html", {"form": form})

        # Pobiera oczyszczone dane z formularza
        cleaned_data = form.cleaned_data

        try:
            with transaction.atomic():
                # Pobiera istniejący adres lub tworzy nowy, jeśli nie istnieje
                adres, created = Adres.objects.get_or_create(
                    ulica=cleaned_data["ulica"],
                    numer_domu=cleaned_data["numer_domu"],
                    kod_pocztowy=cleaned_data["kod_pocztowy"],
                    miejscowosc=cleaned_data["miejscowosc"]
                )

                # Tworzy nowy obiekt WniosekBudowlany w bazie danych
                WniosekBudowlany.objects.create(
                    wnioskodawca=request.user,
                    tytul=cleaned_data["tytul"],
                    opis_budowy=cleaned_data["opis_budowy"],
                    adres_dzialki=adres,
                    status="oczekuje" # Ustawia początkowy status wniosku na "oczekuje"
                )
            # Po pomyślnym zapisaniu, przekierowuje do strony potwierdzenia złożenia wniosku
            return redirect("budownictwo:wniosek_zlozony")
        except Exception as e:
            # Obsługa błędów podczas zapisu do bazy danych
            # Możesz zalogować błąd 'e' dla celów debugowania
            return render(
                request,
                "budownictwo/zloz_wniosek_budowlany.html",
                {
                    "form": form,
                    "blad": "Wystąpił błąd podczas zapisu wniosku. Spróbuj ponownie.",
                },
            )


class WniosekZlozonyView(LoginRequiredMixin, WnioskodawcaMixin, View):
    """Widok informujący o pomyślnym złożeniu wniosku."""
    def get(self, request):
        return render(request, "budownictwo/wniosek_zlozony.html")


class ListaWnioskowBudowlanychView(LoginRequiredMixin, View):
    """Widok wyświetlający listę wniosków budowlanych w zależności od roli użytkownika."""
    def get(self, request):
        user = request.user
        is_budownictwo = False
        is_inspektor = False
        wnioski = []

        # Sprawdza, czy użytkownik jest Urzędnikiem ds. budownictwa
        if user.groups.filter(name="Urzędnik ds. budownictwa").exists():
            # Urzędnik widzi wnioski ze status "oczekuje"
            wnioski = WniosekBudowlany.objects.filter(status="oczekuje")
            is_budownictwo = True
        # Sprawdza, czy użytkownik jest Inspektorem nadzoru budowlanego
        elif user.groups.filter(name="Inspektor nadzoru budowlanego").exists():
            # Inspektor widzi wnioski ze status "zweryfikowany"
            wnioski = WniosekBudowlany.objects.filter(status="zweryfikowany")
            is_inspektor = True
        else:
            # Jeśli użytkownik nie ma odpowiednich uprawnień, rzuca błąd dostępu
            raise PermissionDenied("Nie masz dostępu do listy wniosków.")

        return render(request, "budownictwo/lista_wnioskow.html", {
            "wnioski": wnioski,
            "is_budownictwo": is_budownictwo,
            "is_inspektor": is_inspektor,
        })


class WeryfikujWniosekView(LoginRequiredMixin, UrzednikBudowlanyMixin, View):
    """Widok dla Urzędnika ds. budownictwa do weryfikacji wniosku."""
    def get(self, request, pk):
        # Pobiera wniosek po PK lub zwraca 404
        wniosek = get_object_or_404(WniosekBudowlany, pk=pk)
        # Tworzy formularz weryfikacji z danymi istniejącego wniosku
        form = WeryfikujWniosekBudowlanyForm(instance=wniosek)
        return render(request, "budownictwo/rozpatrz_wniosek.html", {"form": form, "wniosek": wniosek})

    def post(self, request, pk):
        # Pobiera wniosek po PK
        wniosek = get_object_or_404(WniosekBudowlany, pk=pk)
        # Tworzy formularz z danymi POST i instancją wniosku
        form = WeryfikujWniosekBudowlanyForm(request.POST, instance=wniosek)

        if form.is_valid():
            # Jeśli wniosek ma zostać zaakceptowany
            if "accept" in request.POST:
                wniosek.status = "zweryfikowany" # Zmienia status na "zweryfikowany"
                wniosek.powod_odrzucenia = "" # Czyści powód odrzucenia
            # Jeśli wniosek ma zostać odrzucony
            elif "reject" in request.POST:
                reason = form.cleaned_data.get("powod_odrzucenia", "").strip()
                # Wymaga podania powodu odrzucenia
                if not reason:
                    form.add_error("powod_odrzucenia", "Podaj powód odrzucenia")
                    return render(request, "budownictwo/rozpatrz_wniosek.html", {"form": form, "wniosek": wniosek})
                wniosek.status = "odrzucony" # Zmienia status na "odrzucony"

            wniosek.save() # Zapisuje zmiany w wniosku
            return redirect("budownictwo:lista") # Przekierowuje do listy wniosków

        # Jeśli formularz nie jest prawidłowy, ponownie renderuje stronę z błędami
        return render(request, "budownictwo/rozpatrz_wniosek.html", {"form": form, "wniosek": wniosek})


class DecyzjaInspektoraView(LoginRequiredMixin, InspektorNadzoruMixin, View):
    """Widok dla Inspektora nadzoru budowlanego do podjęcia decyzji o wniosku."""
    def get(self, request, pk):
        # Pobiera wniosek po PK ze status "zweryfikowany" lub zwraca 404
        wniosek = get_object_or_404(WniosekBudowlany, pk=pk, status="zweryfikowany")
        # Tworzy formularz decyzji inspektora z danymi istniejącego wniosku
        form = DecyzjaInspektoraForm(instance=wniosek)
        return render(request, "budownictwo/decyzja_inspektora.html", {"form": form, "wniosek": wniosek})

    def post(self, request, pk):
        # Pobiera wniosek po PK
        wniosek = get_object_or_404(WniosekBudowlany, pk=pk, status="zweryfikowany")
        # Tworzy formularz z danymi POST i instancją wniosku
        form = DecyzjaInspektoraForm(request.POST, instance=wniosek)

        if form.is_valid():
            # Jeśli wniosek ma zostać zaakceptowany
            if "accept" in request.POST:
                wniosek.status = "zatwierdzony" # Zmienia status na "zatwierdzony"
                wniosek.powod_odrzucenia = "" # Czyści powód odrzucenia
            # Jeśli wniosek ma zostać odrzucony
            elif "reject" in request.POST:
                reason = form.cleaned_data.get("powod_odrzucenia", "").strip()
                # Wymaga podania powodu odrzucenia
                if not reason:
                    form.add_error("powod_odrzucenia", "Podaj powód odrzucenia")
                    return render(request, "budownictwo/decyzja_inspektora.html", {"form": form, "wniosek": wniosek})
                wniosek.status = "odrzucony" # Zmienia status na "odrzucony"

            wniosek.save() # Zapisuje zmiany w wniosku
            return redirect("budownictwo:lista") # Przekierowuje do listy wniosków

        # Jeśli formularz nie jest prawidłowy, ponownie renderuje stronę z błędami
        return render(request, "budownictwo/decyzja_inspektora.html", {"form": form, "wniosek": wniosek})

