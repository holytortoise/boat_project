import os
import datetime
import dateutil.relativedelta as relativedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import models as m

from reservierung import models


class Command(BaseCommand):
    help = "Entfernen alter Reservierungen"

    def add_arguments(self,parser):
        pass

    def handle(self, *args, **options):
        alte_reservierungen()


def alte_reservierungen():
    """
    Entfernt alte Reservierungen
    """
    reservierungen = models.Reservierung.objects.all()
    for reservierung in reservierungen:
        if relativedelta.relativedelta(datetime.datetime.now(),reservierung.e_Datum).months > 2:
            reservierung.delete()
