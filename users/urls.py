from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='RegisterView'),
    path('profile/', views.ProfileView.as_view(), name='ProfileView'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('settings/', views.SettingsView.as_view(), name='SettingsView'),
    path('settings1/', views.Settings1View.as_view(), name='Settings1View'),
]