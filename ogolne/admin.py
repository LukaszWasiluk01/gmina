from django.contrib import admin

from .models import Adres, Mieszkaniec

# Register your models here.

admin.site.register(Mieszkaniec)
admin.site.register(Adres)
