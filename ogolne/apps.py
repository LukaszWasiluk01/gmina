from django.apps import AppConfig
from django.db.models.signals import post_migrate


class OgolneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ogolne"

    def ready(self):
        import ogolne.signals

        from .signals import create_groups

        post_migrate.connect(create_groups, sender=self)
