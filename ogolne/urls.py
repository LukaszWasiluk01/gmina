from django.urls import path

from .views import IndexView, MojeWnioskiView, PanelUrzędnikaView, WniosekDetailView

app_name = "ogolne"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("panel-urzednika/", PanelUrzędnikaView.as_view(), name="panel_urzednika"),
    path("moje-wnioski/", MojeWnioskiView.as_view(), name="moje_wnioski"),
    path(
        "wniosek/<str:app_label>/<str:model>/<int:pk>/",
        WniosekDetailView.as_view(),
        name="wniosek_detail",
    ),
]
