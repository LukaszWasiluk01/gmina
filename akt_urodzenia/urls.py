from django.urls import path

from . import views

app_name = "akt_urodzenia"

urlpatterns = [
    path(
        "zglos-urodzenie/", views.ZglosUrodzenieView.as_view(), name="zglos_urodzenie"
    ),
    path(
        "zglos-urodzenie/confirm/",
        views.ZglosUrodzenieConfirmView.as_view(),
        name="zglos_urodzenie_confirm",
    ),
    path(
        "lista-zgloszen-urodzen/",
        views.ListaZgloszenUrodzenView.as_view(),
        name="lista_zgloszen_urodzen",
    ),
    path(
        "zglos-urodzenie-detail/<int:pk>/",
        views.ZglosUrodzenieDetailView.as_view(),
        name="zglos_urodzenie_detail",
    ),
]
