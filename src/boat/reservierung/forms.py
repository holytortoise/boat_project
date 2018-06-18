from django import forms
import datetime
from .models import Reservierung,Boot


class ReservierungForm(forms.Form):
    reserviertesBoot = forms.CharField()
    a_Datum = forms.DateField()
    e_Datum = forms.DateField()
    a_Zeit = forms.TimeField(help_text='HH:mm')
    e_Zeit = forms.TimeField(help_text='HH:mm')
