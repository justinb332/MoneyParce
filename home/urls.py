from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('expense/', views.add_expense, name='add_expense'),
    path('settings/', views.settings, name='settings'),
    path('settings/delete/', views.delete_account, name='settings_delete'),
    path('income/', views.add_income, name='add_income'),
    path('settings/reset-data/', views.reset_data, name='reset_data'),
]