from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from django.conf import settings
from taskapp.models import CustomUser


class Command(BaseCommand):
    help = "Command to create default admin"

    def handle(self, *args, **options):
        try:
            CustomUser.objects.create_superuser(email=settings.ADMIN_LOGIN, password=settings.ADMIN_PASSWORD)
            self.stdout.write('Default admin has been created')
        except IntegrityError:
            self.stdout.write('Default admin is already exist')
