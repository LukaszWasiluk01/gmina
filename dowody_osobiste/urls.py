from django.urls import path

from .views import ListaWnioskowView, RozpatrzWniosekView, ZlozWniosekView

app_name = "dowody_osobiste"

urlpatterns = [
    path("zloz/", ZlozWniosekView.as_view(), name="zloz"),
    path("lista/", ListaWnioskowView.as_view(), name="lista"),
    path("rozpatrz/<int:pk>/", RozpatrzWniosekView.as_view(), name="rozpatrz"),
]
