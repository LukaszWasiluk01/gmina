# ogolne/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import IndexView, RejestracjaView, LoginView, MojeWnioskiView, PanelUrzednikaView

app_name = 'ogolne'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('rejestracja/', RejestracjaView.as_view(), name='rejestracja'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('moje-wnioski/', MojeWnioskiView.as_view(), name='moje_wnioski'),
    path('panel-urzednika/', PanelUrzednikaView.as_view(), name='panel_urzednika'),
]