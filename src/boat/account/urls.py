from django.urls import path
from django.contrib.auth import views

app_name = 'account'

urlpatterns = [
    path('login',views.LoginView.as_view(template_name="account/login.html"),name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('password_change/done',views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"),
    name='password-change-done'),
    path('password-change',views.PasswordChangeView.as_view(template_name="account/password_change.html"),name="password-change"),
    
]
