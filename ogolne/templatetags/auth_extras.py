from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Niestandardowy filtr szablonu, który sprawdza,
    czy użytkownik należy do określonej grupy.
    Użycie w szablonie: {{ user|has_group:"Nazwa Grupy" }}
    """
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()