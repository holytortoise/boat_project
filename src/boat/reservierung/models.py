from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import Settings
from django.urls import reverse

import datetime
# Create your models here.


class Boot(models.Model):
    name = models.CharField(max_length=255)

    def get_name(self):
        return "{}".format(self.name)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name_plural = "Boote"

class Reservierung(models.Model):
    reserviert_von = models.ForeignKey(User, related_name="Reserviert",on_delete=models.CASCADE)
    reserviertesBoot = models.ForeignKey(Boot,on_delete=models.CASCADE)
    a_Datum = models.DateField("Start Datum", default=datetime.date.today)
    e_Datum = models.DateField("End Datum", default=datetime.date.today)


    def get_absolute_url(self):
        return reverse('reservierung:index')

    def create_choice(self):
        choice = []
        try:
            boats = Boot.objects.all()
            for boat in boats:
                choice.append((boat.id, boat.get_name()))
        except:
            pass
        return choice

    def __str__(self):
        return "{} {} {} {}".format(self.reserviert_von,self.reserviertesBoot,
        self.a_Datum,self.e_Datum)


    class Meta:
        verbose_name_plural = 'Reservierungen'
        ordering = ['reserviertesBoot','a_Datum']
