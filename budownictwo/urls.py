from django.urls import path
from .views import (
    ZlozWniosekBudowlanyView, PotwierdzWniosekBudowlanyView, WniosekZlozonyView,
    ListaWnioskowBudowlanychView, WeryfikujWniosekView, DecyzjaInspektoraView,
)

app_name = "budownictwo"

urlpatterns = [
    path("zloz/", ZlozWniosekBudowlanyView.as_view(), name="zloz_wniosek_budowlany"),
    path("potwierdz/", PotwierdzWniosekBudowlanyView.as_view(), name="potwierdz_wniosek_budowlany"),
    path("zlozony/", WniosekZlozonyView.as_view(), name="wniosek_zlozony"),
    path("lista/", ListaWnioskowBudowlanychView.as_view(), name="lista"),
    path("weryfikuj/<int:pk>/", WeryfikujWniosekView.as_view(), name="weryfikuj"),
    path("decyzja/<int:pk>/", DecyzjaInspektoraView.as_view(), name="decyzja_inspektora"),
]
