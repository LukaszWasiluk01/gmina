import random

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from ogolne.models import Mieszkaniec

from .forms import ZgloszenieUrodzeniaForm
from .models import ZgloszenieUrodzenia

# Create your views here.


class ZglosUrodzenieView(LoginRequiredMixin, View):
    def get(self, request):
        form = ZgloszenieUrodzeniaForm()
        return render(request, "akt_urodzenia/zglos_urodzenie.html", {"form": form})

    def post(self, request):
        form = ZgloszenieUrodzeniaForm(request.POST)

        if request.POST.get("zmien"):
            return render(request, "akt_urodzenia/zglos_urodzenie.html", {"form": form})

        if form.is_valid():
            return render(
                request,
                "akt_urodzenia/zglos_urodzenie_confirm.html",
                {"form": form},
            )

        return render(request, "akt_urodzenia/zglos_urodzenie.html", {"form": form})


class ZglosUrodzenieConfirmView(LoginRequiredMixin, View):
    def post(self, request):
        form = ZgloszenieUrodzeniaForm(request.POST)
        if not form.is_valid():
            return render(request, "akt_urodzenia/zglos_urodzenie.html", {"form": form})

        dane = form.cleaned_data
        pesel = self.generuj_pesel(dane["data_urodzenia"], dane["plec"])

        try:
            with transaction.atomic():
                m = Mieszkaniec.objects.create(
                    imie=dane["imie"],
                    nazwisko=dane["nazwisko"],
                    pesel=pesel,
                    data_urodzenia=dane["data_urodzenia"],
                    plec=dane["plec"],
                    adres=request.user.mieszkaniec.adres,
                    aktywny=False,
                )

                if request.user.mieszkaniec.plec == "M":
                    m.ojciec = request.user.mieszkaniec
                    m.matka = Mieszkaniec.objects.get(pesel=dane["pesel_rodzica"])
                else:
                    m.matka = request.user.mieszkaniec
                    m.ojciec = Mieszkaniec.objects.get(pesel=dane["pesel_rodzica"])

                m.save()

                ZgloszenieUrodzenia.objects.create(
                    wnioskodawca=request.user,
                    tytul="Zgłoszenie urodzenia",
                    mieszkaniec=m,
                    data_urodzenia=dane["data_urodzenia"],
                )
        except Exception as e:
            return render(
                request,
                "akt_urodzenia/zglos_urodzenie.html",
                {
                    "form": form,
                    "blad": "Wystąpił błąd podczas zapisu. Spróbuj ponownie.",
                },
            )

        return render(request, "akt_urodzenia/zglos_urodzenie_done.html")

    @staticmethod
    def generuj_pesel(data_urodzenia, plec):
        rok = data_urodzenia.year
        miesiac = data_urodzenia.month
        dzien = data_urodzenia.day

        if 1900 <= rok < 2000:
            miesiac += 0
        elif 2000 <= rok < 2100:
            miesiac += 20
        elif 2100 <= rok < 2200:
            miesiac += 40
        elif 1800 <= rok < 1900:
            miesiac += 80
        elif 2200 <= rok < 2300:
            miesiac += 60

        pesel = f"{rok % 100:02d}{miesiac:02d}{dzien:02d}"

        # Losowe cyfry
        for _ in range(4):
            pesel += str(random.randint(0, 9))

        # Płeć – ostatnia cyfra parzysta (K) lub nieparzysta (M)
        ostatnia = random.randrange(0, 10, 2 if plec == "K" else 1)
        pesel = pesel[:-1] + str(ostatnia)

        # Cyfra kontrolna
        wagi = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        suma = sum(int(pesel[i]) * wagi[i] for i in range(10))
        kontrolna = (10 - (suma % 10)) % 10
        pesel += str(kontrolna)

        return pesel


class ListaZgloszenUrodzenView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(
            name="Urzędnik ds. rejestru stanu cywilnego"
        ).exists()

    def handle_no_permission(self):
        raise PermissionDenied("Nie masz dostępu listy tych wniosków.")

    def get(self, request):
        zgloszenia = ZgloszenieUrodzenia.objects.filter(status="oczekuje")
        return render(
            request, "akt_urodzenia/lista_urodzen.html", {"zgloszenia": zgloszenia}
        )


class ZglosUrodzenieDetailView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.groups.filter(
            name="Urzędnik ds. rejestru stanu cywilnego"
        ).exists()

    def handle_no_permission(self):
        raise PermissionDenied("Nie masz dostępu do tego wniosku.")

    def get(self, request, pk):
        z = get_object_or_404(ZgloszenieUrodzenia, pk=pk)
        return render(
            request, "akt_urodzenia/rozpatrz_zgloszenie_detail.html", {"z": z}
        )

    def post(self, request, pk):
        z = get_object_or_404(ZgloszenieUrodzenia, pk=pk)

        if "accept" in request.POST:
            z.status = "zaakceptowane"
            z.mieszkaniec.aktywny = True
            z.mieszkaniec.save()
            z.save()
            return render(
                request,
                "akt_urodzenia/rozpatrz_zgloszenie_detail_done.html",
                {"z": z},
            )

        elif "reject" in request.POST:
            reason = request.POST.get("reason", "").strip()
            if not reason:
                return render(
                    request,
                    "akt_urodzenia/rozpatrz_zgloszenie_detail.html",
                    {
                        "z": z,
                        "error": "Podaj powód odrzucenia.",
                        "show_reason": True,
                    },
                )

            z.status = "odrzucone"
            z.powod_odrzucenia = reason
            z.mieszkaniec.aktywny = False
            z.mieszkaniec.save()
            z.save()
            return render(
                request,
                "akt_urodzenia/rozpatrz_zgloszenie_detail_done.html",
                {"z": z},
            )

        return redirect("akt_urodzenia:lista_zgloszen_urodzen")
