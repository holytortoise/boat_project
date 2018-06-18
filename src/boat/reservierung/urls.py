from django.urls import path

from . import views

app_name = 'reservierung'
urlpatterns = [
    path('',views.index,name='index'),
    path('reservierung', views.ReservierungsList.as_view(),name='reservierung-list'),
]
