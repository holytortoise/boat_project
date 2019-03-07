from django import forms
from django.contrib.auth.models import User
import datetime
from .models import Reservierung,Boot,Images

def create_choice():
    choice = []
    try:
        boats = Boot.objects.all()
        for boat in boats:
            choice.append((boat.id, boat.get_name()))
    except:
        pass
    return choice

class ReservierungForm(forms.Form):
    reserviertesBoot = forms.ChoiceField(choices=create_choice())
    a_Datum = forms.DateField(label='Anfangs Datum')
    e_Datum = forms.DateField(label='End Datum')
    ziel = forms.CharField(label='Ziel')
    anlegeplatz = forms.CharField(label='Anlegeplatz')


    def clean(self):
        cleaned_data = super(ReservierungForm, self).clean()
        a_Datum = cleaned_data.get('a_Datum')
        e_Datum = cleaned_data.get('e_Datum')
        boot = Boot.objects.get(cleaned_data.get('reserviertesBoot'))

        if boot.sperrung == True:
            raise forms.ValidationError("Das gewählte Boot ist GESPERRT")
        if a_Datum and e_Datum:
            # Only do something if both fields are valid so far
            if a_Datum < datetime.date.today():
                raise forms.ValidationError("Anfangsdatum kann nicht in der Vergangenheit liegen.")
            if a_Datum > e_Datum:
                raise forms.ValidationError("Enddatum kann nicht vor Anfangsdatum sein.")


class BootForm(forms.ModelForm):
    name = forms.CharField(label='Name')
    info = forms.CharField(label='Information')

    def clean(self):
        cleaned_Data = super(BootForm, self).clean()
        name = cleaned_Data.get('name')
        boats = Boot.objects.all()
        for boat in boats:
            if boat.name == name:
                raise forms.ValidationError('Boot existiert bereits')

    class Meta:
        model = Boot
        fields = ('name','info',)


class ImageForm(forms.ModelForm):
   image = forms.ImageField(label='Image')
   class Meta:
       model = Images
       fields= ('image',)


class InstandsetzungForm(forms.Form):
    eintrag = forms.CharField(label='Eintrag')


class EinweisungForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    einweisung = forms.BooleanField(required=False)
