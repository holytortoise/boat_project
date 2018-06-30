from django import forms
import datetime
from .models import Reservierung,Boot



class ReservierungForm(forms.Form):
    choice = ()
    model = Reservierung()
    choice = model.create_choice()
    reserviertesBoot = forms.ChoiceField(choice)
    a_Datum = forms.DateField(label='Anfangs Datum',initial='Anfangs Datum')
    e_Datum = forms.DateField(label='End Datum')
    a_Zeit = forms.TimeField(label='Anfangs Zeit',help_text='HH:mm')
    e_Zeit = forms.TimeField(label='End Zeit',help_text='HH:mm')


    def clean(self):
        cleaned_data = super(ReservierungForm, self).clean()
        a_Datum = cleaned_data.get('a_Datum')
        e_Datum = cleaned_data.get('e_Datum')
        a_Zeit = cleaned_data.get('a_Zeit')
        e_Zeit = cleaned_data.get('e_Zeit')

        if a_Datum and e_Datum:
            # Only do something if both fields are valid so far
            if a_Datum < datetime.date.today():
                raise forms.ValidationError("Anfangsdatum kann nicht in der Vergangenheit liegen.")
            if a_Datum == datetime.date.today():
                if a_Zeit < datetime.datetime.time():
                    raise forms.ValidationError("Anfangszeit kann nicht in der Vergangenheit liegen.")
            if a_Datum > e_Datum:
                raise forms.ValidationError("Enddatum kann nicht vor Anfangsdatum sein.")
            if a_Datum == e_Datum:
                if a_Zeit > e_Datum:
                    raise forms.ValidationError("Anfangszeit kann nicht nach der Endzeit liegen.")
                if a_Zeit == e_Zeit:
                    raise forms.ValidationError("Anfangs und End Zeit können nicht gleich sein.")
