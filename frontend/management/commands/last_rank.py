from django.core.management.base import BaseCommand
from django.db import connection, transaction

from frontend import models as frontend_models


class Command(BaseCommand):
    help = 'Updates last rank for all servers.'

    def handle(self, *args, **options):
        servers = frontend_models.Server.objects.all().order_by('-vote_count')

        i = 1
        for server in servers:
            server.last_rank = i
            server.save()
            i += 1

        """
        cursor = connection.cursor()
        cursor.execute("UPDATE ...")    # TODO
        transaction.commit_unless_managed()
        """

        self.stdout.write('Last rank updated for all servers.')