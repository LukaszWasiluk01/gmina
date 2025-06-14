# gmina/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ogolne.urls', namespace='ogolne')),
    path('akty/', include('akt_urodzenia.urls', namespace='akt_urodzenia')),
    path('budownictwo/', include('budownictwo.urls', namespace='budownictwo')),
    path('dotacje/', include('dotacje.urls', namespace='dotacje')),
    path('dowody/', include('dowody_osobiste.urls', namespace='dowody_osobiste')),
    path('ludnosc/', include('ewidencja_ludnosci.urls', namespace='ewidencja_ludnosci')),
    path('zbiorniki/', include('ewidencja_zbiornikow.urls', namespace='ewidencja_zbiornikow')),
    path('odpady/', include('odpady.urls', namespace='odpady')),
    path('podatki/', include('podatki.urls', namespace='podatki')),
    path('rejestracja_samochodu/', include('rejestracja_samochodu.urls', namespace='rejestracja_samochodu')),
]