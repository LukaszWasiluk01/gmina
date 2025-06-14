# gmina/gmina/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ogolne.views import IndexView, RejestracjaView

urlpatterns = [
    # Główne ścieżki projektu
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'), # Strona główna
    path('rejestracja/', RejestracjaView.as_view(), name='rejestracja'), # Rejestracja użytkownika
    path('login/', auth_views.LoginView.as_view(template_name='ogolne/login.html'), name='login'), # Logowanie
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'), # Wylogowanie

    # Dołączenie adresów URL z poszczególnych aplikacji z prefiksami
    path('ogolne/', include('ogolne.urls', namespace='ogolne')),
    path('akty-urodzenia/', include('akt_urodzenia.urls', namespace='akt_urodzenia')),
    path('budownictwo/', include('budownictwo.urls', namespace='budownictwo')),
    path('dotacje/', include('dotacje.urls', namespace='dotacje')),
    path('dowody-osobiste/', include('dowody_osobiste.urls', namespace='dowody_osobiste')),
    path('ewidencja-ludnosci/', include('ewidencja_ludnosci.urls', namespace='ewidencja_ludnosci')),
    path('ewidencja-zbiornikow/', include('ewidencja_zbiornikow.urls', namespace='ewidencja_zbiornikow')),
    path('odpady/', include('odpady.urls', namespace='odpady')),
    path('podatki/', include('podatki.urls', namespace='podatki')),
    path('rejestracja-samochodu/', include('rejestracja_samochodu.urls', namespace='rejestracja_samochodu')),
]