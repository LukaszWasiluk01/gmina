from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    IndexView,
    LoginView,
    MojeWnioskiView,
    PanelUrzednikaView,
    RejestracjaView,
)

app_name = "ogolne"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("rejestracja/", RejestracjaView.as_view(), name="rejestracja"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("moje-wnioski/", MojeWnioskiView.as_view(), name="moje_wnioski"),
    path("panel-urzednika/", PanelUrzednikaView.as_view(), name="panel_urzednika"),
]
