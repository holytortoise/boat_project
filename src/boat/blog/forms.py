from django import forms
from django.contrib.auth.models import User
import datetime

class PostCreateForm(forms.Form):
    title = forms.CharField(max_length=200,label='Titel')
    text = forms.TextField(label='Inhalt')
