from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,AccessMixin
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import datetime
from . import models
from . import forms
# Create your views here.

class ReservierungsList(LoginRequiredMixin, ListView):
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    queryset = models.Reservierung.objects.order_by('a_Datum')
    context_object_name = 'reservierungen'


class ReservierungDelete(LoginRequiredMixin,PermissionRequiredMixin,AccessMixin, DeleteView):
    permission_required = 'reservierung.can_delete_reservierung'
    raise_exception = True
    login_url = 'account:login'
    redirect_field_name : 'redirect_to'
    model = models.Reservierung
    success_url = reverse_lazy('reservierung:list')
    template_name = 'reservierung/reservierung_delete.html'


class ReservierungDetail(LoginRequiredMixin, DetailView):
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    model = models.Reservierung
    context_object_name = 'reservierung'
    template_name = 'reservierung/reservierung_detail.html'


class BootListe(LoginRequiredMixin, ListView):
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    queryset = models.Boot.objects.order_by('name')
    context_object_name = 'boote'


class EinweisungList(LoginRequiredMixin, ListView):
    login_url='account:login'
    redirect_field_name ='redirect_to'
    queryset = models.Einweisung.objects.order_by('boot')
    context_object_name = 'einweisungen'


class EinweisungDelete(LoginRequiredMixin,PermissionRequiredMixin,AccessMixin, DeleteView):
    permission_required = 'reservierung.can_delete_einweisung'
    raise_exception = True
    login_url = 'account:login'
    redirect_field_name : 'redirect_to'
    model = models.Einweisung
    success_url = reverse_lazy('reservierung:einweisung-list')
    template_name = 'reservierung/einweisung_delete.html'

class EinweisungDetail(LoginRequiredMixin, DetailView):
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    model = models.Einweisung
    context_object_name = 'einweisung'
    template_name = 'reservierung/einweisung_detail.html'

class EinweisungUpdate(LoginRequiredMixin,PermissionRequiredMixin,AccessMixin, UpdateView):
    permission_required = 'reservierung.can_change_einweisung'
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    model = models.Einweisung
    success_url = reverse_lazy('reservierung:einweisung-list')
    template_name = 'reservierung/einweisung_update.html'
    fields = ['einweisung']


class InstandsetzungDelete(LoginRequiredMixin, DeleteView):
    login_url = 'account:login'
    redirect_field_name : 'redirect_to'
    model = models.Instandsetzung
    success_url = reverse_lazy('reservierung:boote')
    template_name = 'reservierung/einweisung_delete.html'

@login_required(login_url='account:login')
def boot_liste(request):
    liste = []
    boats = models.Boot.objects.all()
    for boat in boats:
        images = models.Images.objects.filter(boot=boat)
        liste.append(images)
    print(liste)
    return render(request, 'boot_list.html',{'liste':liste})

@login_required(login_url='account:login')
def index(request):
    today = datetime.date.today()
    end = today + datetime.timedelta(30)
    boats = models.Boot.objects.all()
    if boats.exists():
        boats_return = []
        for boat in boats:
            boat_return = []
            reservierungen = models.Reservierung.objects.filter(
                reserviertesBoot=boat).order_by('a_Datum')
            if reservierungen.exists():
                for reservierung in reservierungen:
                    if reservierung.a_Datum < today and reservierung.e_Datum >= today:
                        boat_return.append(reservierung)
                    if reservierung.a_Datum >= today and reservierung.a_Datum < end:
                        boat_return.append(reservierung)
                if len(boat_return) != 0:
                    boats_return.append(boat_return)
            else:
                reservierungen = None
        if len(boats_return) == 0:
            boats_return = None
    context_dict = {'boats_return':boats_return,'reserv':reservierungen,'today':today,'end':end}
    return render(request,'index.html', context_dict)

    return render(request, 'index.html')

@login_required(login_url='account:login')
def reservierung_form(request):
    """
    Diese Funktion ist für die Reservierung zuständig
    """
    nutzer = request.user
    moeglich = False
    reserv = None
    free_boats = None
    if request.method == 'POST':
        form = forms.ReservierungForm(data=request.POST)
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
                        elif reservierung.a_Datum > form.cleaned_data.get("e_Datum"):
                            moeglich = True
                        elif reservierung.a_Datum == form.cleaned_data.get("e_Datum"):
                            moeglich = False
                            reserv = reservierung
                            break
                        elif reservierung.e_Datum == form.cleaned_Data.get("a_Datum"):
                            moeglich = False
                            reserv = reservierung
                            break
            else:
                moeglich = True
            if moeglich:
                staff = User.objects.filter(is_staff=True)
                message = "{} hat von {} bis {} das Boot {} reserviert.".format(request.user,form.cleaned_data.get('a_Datum'),form.cleaned_data.get('e_Datum'),form.cleaned_data.get('reserviertesBoot'))
                email_from = settings.EMAIL_HOST_USER
                print(staff)
                print(message)
                print(email_from)
                for staff_user in staff:
                    print('Sending Email...')
                    send_mail('Reservierung',message,email_from,[staff_user.email,])
                    print('Email sent')
                reserv = models.Reservierung()
                reserv.reserviert_von = request.user
                reserv.reserviertesBoot = models.Boot.objects.get(id=form.cleaned_data.get("reserviertesBoot"))
                reserv.a_Datum = form.cleaned_data.get("a_Datum")
                reserv.e_Datum = form.cleaned_data.get("e_Datum")
                reserv.save()

                return HttpResponseRedirect(reverse('reservierung:index'))
            else:
                boats = models.Boot.objects.exclude(id=form.cleaned_data.get("reserviertesBoot"))
                if boats.exists():
                    for boat in boats:
                        boats_reservs = models.Reservierung.objects.filter(reserviertesBoot=boat)
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
                                        free_boat = False
                                        break
                                    elif boat_reserv.a_Datum > form.cleaned_data.get("e_Zeit"):
                                        free_boat = True
                                    elif boat_reserv.a_Datum == form.cleaned_data.get("e_Datum"):
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

@login_required(login_url='account:login')
def reservierung_user(request):
    user = request.user
    boats = models.Boot.objects.all()
    boats_return = []

    for boat in boats:
        boat_return = []
        reservierungen = models.Reservierung.objects.filter(
            reserviertesBoot=boat).order_by('a_Datum')
        for reservierung in reservierungen:
            if reservierung.reserviert_von == user:
                boat_return.append(reservierung)
        boats_return.append(boat_return)
    return render(request, 'reservierung/reservierung_user.html',{'user':user,'boats_return':boats_return})

@login_required(login_url='account:login')
@permission_required('reservierung.can_add_boot', raise_exception=True)
def boot_erstellen(request):

    ImageFormSet = modelformset_factory(models.Images,form=forms.ImageForm, extra=3)

    if request.method == 'POST':
        postForm = forms.BootForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=models.Images.objects.none())

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = models.Images(boot=models.Boot.objects.get(name=postForm.cleaned_data.get('name')),image=image)
                photo.save()
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = forms.BootForm()
        formset = ImageFormSet(queryset=models.Images.objects.none())
    return render(request, 'boot_erstellen.html',
                {'postForm':postForm,'formset':formset})

@login_required(login_url='account:login')
def boot_details(request,pk):
    boat = models.Boot.objects.get(id=pk)
    images = models.Images.objects.filter(boot=boat)
    einweisung = models.Einweisung.objects.filter(boot=boat)
    instandsetzung = models.Instandsetzung.objects.filter(boot=boat)
    context_dict = {'boat':boat,'images':images,'einweisung':einweisung,'instandsetzung':instandsetzung}
    return render(request, 'boot_details.html',context_dict)

@login_required(login_url='account:login')
def instandsetzung(request,pk):
    boat = models.Boot.objects.get(id=pk)
    nutzer = request.user
    einträge = models.Instandsetzung.objects.filter(boot=boat)
    context_dict = {'boat':boat,'einträge':einträge}
    if request.method == 'POST':
        form = forms.InstandsetzungForm(data=request.POST)
        if form.is_valid():
            instandsetzung = models.Instandsetzung()
            instandsetzung.user = nutzer
            instandsetzung.boot = boat
            instandsetzung.eintrag = form.cleaned_data.get("eintrag")
            instandsetzung.save()
            return HttpResponseRedirect(reverse('reservierung:boote'))
    else:
        form = forms.InstandsetzungForm()
        context_dict['form'] = form
    return render(request, 'instandsetzung.html', context_dict)

@login_required(login_url='account:login')
@permission_required('reservierung.can_add_einweisung', raise_exception=True)
def einweisung(request,pk):
    boat = models.Boot.objects.get(id=pk)
    nutzer = request.user
    einweisungen = models.Einweisung.objects.filter(boot=boat)
    context_dict = {'boat':boat,'einweisungen':einweisungen}
    if request.method == 'POST':
        form = forms.EinweisungForm(data=request.POST)
        if form.is_valid():
            info = models.Einweisung.objects.filter(user=nutzer,boot=boat)
            if info.exists():
                return HttpResponseRedirect(reverse('reservierung:boote'))
            else:
                einweisung = models.Einweisung()
                einweisung.user = form.cleaned_data.get('user')
                einweisung.boot = boat
                einweisung.einweisung = form.cleaned_data.get('einweisung')
                einweisung.save()
                return HttpResponseRedirect(reverse('reservierung:boote'))
    else:
        form = forms.EinweisungForm()
        context_dict['form'] = form
    return render(request, 'einweisung.html', context_dict)
