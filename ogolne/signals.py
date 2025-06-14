# lukaszwasiluk01/gmina/gmina-master/ogolne/signals.py

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.conf import settings

# Pełna i poprawna lista wszystkich grup/ról w systemie
GROUPS = [
    'Wnioskodawca', 'Wójt', 'Urzędnik ds. wydawania dowodów osobistych',
    'Urzędnik ds. rejestru stanu cywilnego', 'Urzędnik ds. rejestracji samochodów',
    'Urzędnik ds. podatków', 'Urzędnik ds. gospodarki odpadami',
    'Urzędnik ds. ewidencji zbiorników', 'Urzędnik ds. ewidencji ludności',
    'Urzędnik ds. dotacji', 'Urzędnik ds. budownictwa', 'Skarbnik gminy',
    'Pracownik ds. statystyki', 'Komisja ds. dotacji', 'Inspektor nadzoru budowlanego'
]

def create_groups(sender, **kwargs):
    for group_name in GROUPS:
        Group.objects.get_or_create(name=group_name)
    print("Utworzono grupy użytkowników.")

# Sygnał do tworzenia grup po migracji
post_migrate.connect(create_groups)

# Sygnał do automatycznego przypisywania nowych użytkowników do grupy "Wnioskodawca"
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        try:
            group = Group.objects.get(name='Wnioskodawca')
            instance.groups.add(group)
        except Group.DoesNotExist:
            # Na wypadek, gdyby grupa jeszcze nie istniała
            pass