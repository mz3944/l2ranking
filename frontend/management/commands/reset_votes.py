from django.core.management.base import BaseCommand

from frontend import models as frontend_models


class Command(BaseCommand):
    help = 'Resets votes for all servers (sets to zero).'

    def handle(self, *args, **options):
        frontend_models.Server.objects.update(vote_count=0)
        self.stdout.write('Votes have been reset.')