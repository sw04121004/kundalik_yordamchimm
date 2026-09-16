import os
import sys
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def auto_seed_services(sender, **kwargs):
    try:
        from apps.services.management.commands.seed_services import Command
        Command().handle()
    except Exception:
        pass


class ServicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.services"
    label = "services"

    def ready(self):
        post_migrate.connect(auto_seed_services, sender=self)

        # Run automatically on 'python manage.py runserver'
        if any("runserver" in arg for arg in sys.argv):
            if os.environ.get("RUN_MAIN") == "true":
                try:
                    from apps.services.management.commands.seed_services import Command
                    Command().handle()
                except Exception:
                    pass
