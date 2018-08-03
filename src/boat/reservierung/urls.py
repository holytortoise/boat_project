from django.urls import path

from . import views

app_name = 'reservierung'
urlpatterns = [
    path('',views.index,name='index'),
    path('reservierung', views.ReservierungsList.as_view(),name='list'),
    path('reservierung/form/', views.reservierung_form, name ='form'),
    path('reservierung/<int:pk>/', views.ReservierungDetail.as_view(), name='detail'),
    path('reservierung/<int:pk>/delete/', views.ReservierungDelete.as_view(), name='delete'),
    #path('reservierung/boote/', views.BootListe.as_view(), name='boote'),
    path('reservierung/boote/', views.boot_liste, name='boote'),
    path('reservierung/user/', views.reservierung_user, name='user'),
    path('reservierung/boot_erstellen', views.boot_erstellen, name='boot-erstellen'),
    path('reservierung/boote/details/<int:pk>/', views.boot_details, name='boot-details'),
    path('reservierung/boote/instandsetzung/<int:pk>/',views.instandsetzung, name='instandsetzung'),
    path('reservierung/einweisungen/', views.EinweisungList.as_view(), name='einweisung-list'),
    path('reservierung/einweisung/<int:pk>/', views.einweisung, name='einweisung'),
]
