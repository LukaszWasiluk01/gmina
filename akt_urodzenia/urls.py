from django.urls import path

from .views import ListaZgloszenUrodzenView, ZglosUrodzenieView, ZgloszenieDetailView

app_name = "akt_urodzenia"

urlpatterns = [
    path("zglos/", ZglosUrodzenieView.as_view(), name="zglos_urodzenie"),
    path("lista/", ListaZgloszenUrodzenView.as_view(), name="lista_zgloszen"),
    path(
        "zgloszenie/<int:pk>/", ZgloszenieDetailView.as_view(), name="zgloszenie_detail"
    ),
]
