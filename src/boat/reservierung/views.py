from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,FormView

from . import models
from . import forms
# Create your views here.
def index(request):
    current_week = datetime.date.today().isocalendar()[1]
    current_year = datetime.date.today().isocalendar()[0]
    is_week = None
    if request.method == 'POST':
        jahr = int(request.POST['jahr'])
        woche = int(request.POST['woche'])
        if request.POST.__contains__('next_week'):
            if woche == datetime.date(jahr,12,28).isocalendar()[1]:
                woche = 1
                jahr = jahr + 1
            else:
                woche = woche + 1
        if request.POST.__contains__('last_week'):
            if woche == 1:
                jahr = jahr - 1
                woche = datetime.date(jahr,12,28).isocalendar()[1]
            else:
                woche = woche - 1
    else:
        jahr = datetime.date.today().isocalendar()[0]
        woche = datetime.date.today().isocalendar()[1]
    if woche == current_week and jahr == current_year:
        is_week = True
    if woche != current_week or jahr != current_year:
        is_week = False

    datum = str(jahr)+'-W'+str(woche)
    r = datetime.datetime.strptime(datum +'-0',"%Y-W%W-%w")
    start = r -datetime.timedelta(days=r.weekday())
    end = start + datetime.timedelta(days=6)
    start = start.strftime('%d.%m')
    end = end.strftime('%d.%m')

    boats = models.Boat.objects.all()
    boats_return = []
    for boat in boats:
        boat_return = []
        reservierungen = models.Reservierung.objects.filter(
            reserviertesBoot=boat).order_by('a_Datum')
        for reservierung in reservierungen:
            if reservierung.a_Datum.isocalendar()[1] < woche and woche < reservierung.e_Datum.isocalendar()[1]:
                boat_reaturn.append(reservierung)
            if ((reservierung.a_Datum.isocalendar()[1] < woche and reservierung.a_Datum.isocalendar()[0] == jahr)
                or (reservierung.e_Datum.isocalendar()[1] == woche and reservierung.e_Datum.isocalendar()[0] == jahr)):
                boat_return.append(reservierung)
        if len(boat_return) != 0:
            boats_return.append(boat_return)
    if len(boats_return) == 0:
        boats_return = None
    context_dict = {'boats_return':boats_return,'reserv':reservierungen,'woche':woche,
    'jahr':jahr,'current_week':current_week,'current_year':current_year,
    'is_week':is_week,'start':start,'end':end}
    return render(request, 'index.html', context_dict)


    return render(request, 'index.html')

class ReservierungsList(ListView):
    queryset = models.Reservierung.objects.order_by('a_Datum','a_Zeit')
    context_object_name = 'reservierungen'



def reservierung_form(request):
    """
    Diese Funktion ist für die Reservierung zuständig
    """
    nutzer = request.user
    moeglich
    if request.method == 'POST':
        forms = forms.ReservierungForm(data=request.post)
        if form.is_valid():
            free_boats = []
            reservierungen = models.Reservierung.objects.filter(
                reserviertesBoot=form.cleaned_data.get("reserviertesBoot"))
            if reservierungen.exists():
                for reservierung in reservierungen:
                    if reservierung.a_Datum < form.cleaned_data.get("a_Datum") and form.cleaned_data.get("a_Datum") < reservierung.e_Datum:
                        moeglich = False
                        reserv = reservierung
                        break
                    else:
                        if reservierung.e_Datum < form.cleaned_data.get("a_Datum"):
                            moeglich = True
                        elif reservierung.e_Datum == form.cleaned_data.get("a_Datum"):
                            if reservierung.e_Zeit <= form.cleaned_data.get("a_Zeit"):
                                moeglich = True
                            elif reservierung.a_Zeit >= form.cleaned_data.get("e_Zeit"):
                                moeglich = True
                            else:
                                moeglich = False
                                reserv = reservierung
                                break
                        elif reservierung.a_Datum > form.cleaned_data.get("e_Datum"):
                            moeglich = True
                        elif reservierung.a_Datum == form.cleaned_data.get("e_Datum"):
                            if reservierung.a_Zeit > form.cleaned_data.get("e_Zeit"):
                                moeglich = True
                            else:
                                moeglich = False
                                reserv = reservierung
                                break
            else:
                moeglich = True
            if moeglich:
                reserv = models.Reservierung()
                reserv.reserviert_von = request.user
                reserv.reserviertesBoot = models.Boot.objects.get(id=form.cleaned_data.get("reserviertesBoot"))
                reserv.a_Datum = form.cleaned_data.get("a_Datum")
                reserv.e_Datum = form.cleaned_data.get("e_Datum")
                reserv.a_Zeit = form.cleaned_data.get("a_Zeit")
                reserv.e_Zeit = form.cleaned_data.get("e_Zeit")
                reserv.save()
                return HttpResponseRedirect(reverse('reservierung:index'))
            else:
                boats = models.Boat.objects.exclude(id=form.cleaned_data.get("reserviertesBoot"))
                if boats.exists():
                    for boat in boats:
                        boat_reservs = models.Reservierung.objects.filter(reserviertesBoot=boat)
                        if boat_reservs.exists():
                            free_boats = False
                            for boat_reserv in boats_reservs:
                                if boat_reserv.a_Datum < form.cleaned_data.get("a_Datum") and form.cleaned_data.get("a_Datum") < boat_reserv.e_Datum:
                                    free_boat = False
                                    break
                                else:
                                    if boat_reserv.e_Datum < form.cleaned_data.get("a_Datum"):
                                        free_boat = True
                                    elif boat_reserv.e_Datum == form.cleaned_Data.get("a_Datum"):
                                        if boat_reserv.e_Zeit <= form.cleaned_data.get("a_Zeit"):
                                            free_boat = True
                                        else:
                                            free_boat = False
                                            break
                                    elif boat_reserv.a_Datum > form.cleaned_data.get("e_Zeit"):
                                        free_boat = True
                                    elif boat_reserv.a_Datum == form.cleaned_data.get("e_Datum"):
                                        if boat_reserv.a_Zeit > form.cleaned_data.get("e_Zeit"):
                                            free_boat = True
                                        else:
                                            free_boat = False
                                            break
                                if free_boat:
                                    free_boats.append(boat)
                            else:
                                free_boats.append(boat)
                else:
                    free_boats = models.Boat.objects.all()
    else:
        form = forms.ReservierungForm()
    return render(request, 'reservierung/reservierung_form.html',{'form':form,
        'reserv':reserv,'free_boats':free_boats,})


def reservierung_user(request):
    user = request.user
    boats = models.Boat.objects.all()
    boats_return = []

    for boat in boats:
        boat_return = []
        reservierungen = models.Reservierung.objects.filter(
            reserviertesBoot=boat).order_by('a_Datum')
        for reservierung in reservierungen:
            if reservierung.reserviert_von == user:
                boat_return.append(boat)
        boats_return.append(boat_return)
    return render(request, 'reservierung/reservierung_user.html',{'user':user,'boats_return',boats_return})
