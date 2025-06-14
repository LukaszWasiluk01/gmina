from django.urls import path

from .views import GenerujStatystykiView

app_name = "ewidencja_ludnosci"

urlpatterns = [
    path("statystyki/", GenerujStatystykiView.as_view(), name="generuj_statystyki"),
]
