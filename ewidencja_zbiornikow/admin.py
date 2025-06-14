from django.contrib import admin

from .models import DeklaracjaOproznienia, DeklaracjaZbiornika

# Register your models here.

admin.site.register(DeklaracjaZbiornika)
admin.site.register(DeklaracjaOproznienia)
