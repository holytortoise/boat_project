from django import forms
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


    def clean(self):
        cleaned_data = super(ReservierungForm, self).clean()
        a_Datum = cleaned_data.get('a_Datum')
        e_Datum = cleaned_data.get('e_Datum')

        if a_Datum and e_Datum:
            # Only do something if both fields are valid so far
            if a_Datum < datetime.date.today():
                raise forms.ValidationError("Anfangsdatum kann nicht in der Vergangenheit liegen.")
            if a_Datum > e_Datum:
                raise forms.ValidationError("Enddatum kann nicht vor Anfangsdatum sein.")


class BootForm(forms.ModelForm):
    name = forms.CharField()
    instandsetzung = forms.CharField()

    class Meta:
        model = Boot
        fields = ('name','instandsetzung',)


#class ImageForm(forms.ModelForm):
#    image = forms.ImageField(label='Image')
#    class Meta:
#        model = Images
#        fields= ('images',)
