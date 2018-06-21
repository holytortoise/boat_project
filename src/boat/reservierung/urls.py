from django.urls import path

from . import views

app_name = 'reservierung'
urlpatterns = [
    path('',views.index,name='index'),
    path('reservierung', views.ReservierungsList.as_view(),name='list'),
    path('reservierung/form/', views.reservierung_form, name ='form'),
    path('reservierung/<int:pk>/', views.ReservierungDetail.as_view(), name='detail'),
    path('reservierung/<int:pk>/delete/', views.ReservierungDelete.as_view(), name='delete'),
    path('reservierung/user/', views.reservierung_user, name='user'),
]
