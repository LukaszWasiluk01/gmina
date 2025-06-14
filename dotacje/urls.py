from django.urls import path

from .views import (
    ListaWnioskowView,
    PrzelejDotacjeView,
    RozpatrzWniosekKomisjaView,
    RozpatrzWniosekWojtView,
    ZlozWniosekDotacjaView,
)

app_name = "dotacje"

urlpatterns = [
    path("zloz/", ZlozWniosekDotacjaView.as_view(), name="zloz"),
    path("lista/", ListaWnioskowView.as_view(), name="lista"),
    path("komisja/<int:pk>/", RozpatrzWniosekKomisjaView.as_view(), name="komisja"),
    path("wojt/<int:pk>/", RozpatrzWniosekWojtView.as_view(), name="wojt"),
    path("przelej/<int:pk>/", PrzelejDotacjeView.as_view(), name="przelej"),
]
