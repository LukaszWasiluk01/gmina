from django.urls import path

from .views import ListaDeklaracjiView, WyliczOplateView, ZlozDeklaracjeView

app_name = "odpady"

urlpatterns = [
    path("zloz/", ZlozDeklaracjeView.as_view(), name="zloz"),
    path("lista/", ListaDeklaracjiView.as_view(), name="lista"),
    path("wylicz/<int:pk>/", WyliczOplateView.as_view(), name="wylicz"),
]
