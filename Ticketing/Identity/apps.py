from django.apps import AppConfig


from django.apps import AppConfig
from django.db.models.signals import post_migrate

class IdentityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Ticketing.Identity'

    def ready(self):
        from django.contrib.auth.models import Group

        def create_roles(sender, **kwargs):
            Group.objects.get_or_create(name="USER")
            Group.objects.get_or_create(name="ADMIN")

        post_migrate.connect(create_roles, sender=self)
