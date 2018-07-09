from django import forms
import datetime
from .models import Reservierung,Boot



class ReservierungForm(forms.Form):
    reserviertesBoot = forms.ChoiceField(Reservierung().create_choice())
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
