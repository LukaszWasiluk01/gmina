from django.contrib.auth.models import Group, User
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

GROUPS = [
    "Wnioskodawca",
    "Wójt",
    "Urzędnik ds. wydawania dowodów osobistych",
    "Urzędnik ds. rejestru stanu cywilnego",
    "Urzędnik ds. rejestracji samochodów",
    "Urzędnik ds. podatków",
    "Urzędnik ds. gospodarki odpadami",
    "Urzędnik ds. ewidencji zbiorników",
    "Urzędnik ds. ewidencji ludności",
    "Urzędnik ds. dotacji",
    "Urzędnik ds. budownictwa",
    "Skarbnik gminy",
    "Pracownik ds. statystyki",
    "Komisja ds. dotacji",
    "Inspektor nadzoru budowlanego",
]


@transaction.atomic
def create_groups(sender, **kwargs):
    for group_name in GROUPS:
        Group.objects.get_or_create(name=group_name)
