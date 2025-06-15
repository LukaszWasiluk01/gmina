from django.urls import path
from .views import (
    ZlozWniosekDotacjaView,
    ListaWnioskowDotacjeView,
    WniosekDotacjaDetailView,
)

app_name = "dotacje"

urlpatterns = [
    path("zloz/", ZlozWniosekDotacjaView.as_view(), name="zloz_wniosek_dotacja"),
    path("lista/", ListaWnioskowDotacjeView.as_view(), name="lista_wnioskow"),
    path("wniosek/<int:pk>/", WniosekDotacjaDetailView.as_view(), name="wniosek_detail"),
]