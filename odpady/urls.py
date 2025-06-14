# gmina/odpady/urls.py

from django.urls import path
from .views import ZlozDeklaracjeView, ListaDeklaracjiView, WyliczOplateView

app_name = 'odpady'

urlpatterns = [
    # Upewnij się, że nazwa to 'zloz_deklaracje'
    path('zloz/', ZlozDeklaracjeView.as_view(), name='zloz_deklaracje'),
    path('lista/', ListaDeklaracjiView.as_view(), name='lista_deklaracji'),
    path('wylicz/<int:pk>/', WyliczOplateView.as_view(), name='wylicz_oplate'),
]