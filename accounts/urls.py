from django.urls import path
from . import views
from .views import logout_view, CustomLoginView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('reset/', views.reset_password_view, name='reset'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    path('verify-2fa-login/', views.verify_2fa_login, name='verify_2fa_login'),
]