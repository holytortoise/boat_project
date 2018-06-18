from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,FormView

from . import models
from . import forms
# Create your views here.
def index(request):
    return render(request, 'index.html')

class ReservierungsList(ListView):
    queryset = models.Reservierung.objects.order_by('a_Datum','a_Zeit')
    context_object_name = 'reservierungen'



def reservierung_form(request):
    """
    Diese Funktion ist für die Reservierung zuständig
    """
    nutzer = request.user
    
