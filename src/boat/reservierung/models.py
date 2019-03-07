from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import Settings
from django.urls import reverse
import datetime
# Create your models here.


class Boot(models.Model):
    name = models.CharField(max_length=255)
    info = models.TextField(default="Keine Information Verfügbar")
    sperrung = models.BooleanField(default=False)

    def get_name(self):
        return "{}".format(self.name)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name_plural = "Boote"
        ordering = ['name']

class Reservierung(models.Model):
    reserviert_von = models.ForeignKey(User, related_name="Reserviert",on_delete=models.CASCADE)
    reserviertesBoot = models.ForeignKey(Boot,on_delete=models.CASCADE)
    ziel = models.TextField(default="")
    anlegeplatz = models.TextField(default="")
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


class Einweisung(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    boot = models.ForeignKey(Boot,on_delete=models.CASCADE)
    einweisung = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.boot,self.user)

    class Meta:
        verbose_name_plural = "Einweisungen"
        ordering = ['boot']

class Images(models.Model):
    boot = models.ForeignKey(Boot,default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return "{}".format(self.boot.name)

    class Meta:
        ordering = ['boot']

class Instandsetzung(models.Model):
    boot = models.ForeignKey(Boot,default=None,on_delete=models.CASCADE)
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    eintrag = models.TextField()
    geplant_am = models.DateTimeField(default=None,null=True)
    durchfuehrung_durch = models.CharField(max_length=255,null=True,default='Ausstehend')


    def __str__(self):
        return "{} {}".format(self.boot,self.eintrag)

    class Meta:
        ordering = ['boot']
