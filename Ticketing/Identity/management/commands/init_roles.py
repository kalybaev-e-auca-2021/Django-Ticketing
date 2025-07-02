from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Initialize default user roles (groups)'

    def handle(self, *args, **kwargs):
        roles = ['ADMIN', 'USER']
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created role: {role}"))
            else:
                self.stdout.write(f"Role already exists: {role}")
