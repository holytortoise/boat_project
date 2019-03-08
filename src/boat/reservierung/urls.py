from django.urls import path

from . import views

app_name = 'reservierung'
urlpatterns = [
    path('',views.index,name='index'),
    path('reservierung', views.ReservierungsList.as_view(),name='list'),
    path('reservierung/form/', views.reservierung_form, name ='form'),
    path('reservierung/<int:pk>/', views.ReservierungDetail.as_view(), name='detail'),
    path('reservierung/<int:pk>/delete/', views.ReservierungDelete.as_view(), name='delete'),
    path('reservierung/boote/', views.boot_liste, name='boote'),
    path('reservierung/user/', views.reservierung_user, name='user'),
    path('reservierung/boot_erstellen', views.boot_erstellen, name='boot-erstellen'),
    path('reservierung/boote/details/<int:pk>/', views.boot_details, name='boot-details'),
    path('reservierung/boote/instandsetzung/<int:pk>/',views.instandsetzung, name='instandsetzung'),
    path('reservierung/boote/instandsetzung/delete/<int:pk>/', views.InstandsetzungDelete.as_view(), name='instandsetzung-delete'),
    path('reservierung/einweisungen/', views.EinweisungList.as_view(), name='einweisung-list'),
    path('reservierung/einweisung/<int:pk>/', views.einweisung, name='einweisung'),
    path('reservierung/einweisung/löschen/<int:pk>/', views.EinweisungDelete.as_view(), name='einweisung-delete'),
    path('reservierung/einweisung/detail/<int:pk>/', views.EinweisungDetail.as_view(), name='einweisung-detail'),
    path('reservierung/einweisung/update/<int:pk>/', views.EinweisungUpdate.as_view(), name='einweisung-update'),
    path('reservierung/boote/instandsetzung/sperren/<int:pk>/', views.boot_sperren, name='boot-sperren'),
    path('reservierung/boote/instandsetzung/update/<int:pk>', views.InstandsetzungUpdate.as_view(), name='instandsetzung-update'),
    path('reservierung/boote/regeln', views.RegelList.as_view(), name='regel-list'),
    path('reservierung/boote/regel_create', views.RegelCreate.as_view(), name='regel-create'),
    path('reservierung/boote/regel_update/<int:pk>', views.RegelUpdate.as_view(), name='regel-update'),
    path('reservierung/boote/regel_delete/<int:pk>', views.RegelUpdate.as_view(), name='regel-delete'),
]
