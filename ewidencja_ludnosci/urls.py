from django.urls import path

from .views import AktualizujStatystykeView, GenerujStatystykiView

app_name = "ewidencja_ludnosci"

urlpatterns = [
    path("aktualizuj/", AktualizujStatystykeView.as_view(), name="aktualizuj"),
    path("statystyki/", GenerujStatystykiView.as_view(), name="statystyki"),
]
