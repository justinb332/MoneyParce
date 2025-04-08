from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transactions/', views.add_transaction, name='add_transaction'),
    path('settings/', views.settings, name='settings'),
    path('settings/delete/', views.delete_account, name='settings_delete'),
    path('income/', views.add_income, name='add_income'),
    path('settings/reset-data/', views.reset_data, name='reset_data'),
]