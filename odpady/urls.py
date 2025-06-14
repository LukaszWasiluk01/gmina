from django.urls import path

from .views import ListaDeklaracjiView, WyliczOplateView, ZlozDeklaracjeView

app_name = "odpady"

urlpatterns = [
    path("zloz/", ZlozDeklaracjeView.as_view(), name="zloz_deklaracje"),
    path("lista/", ListaDeklaracjiView.as_view(), name="lista_deklaracji"),
    path("wylicz/<int:pk>/", WyliczOplateView.as_view(), name="wylicz_oplate"),
]
