from django.urls import path
from .views import home, add_transaction, settings, delete_account, add_income, reset_data

urlpatterns = [
    path('', home, name='home'),
    path('transactions/', add_transaction, name='add_transaction'),
    path('settings/', settings, name='settings'),
    path('settings/delete/', delete_account, name='settings_delete'),
    path('income/', add_income, name='add_income'),
    path('settings/reset-data/', reset_data, name='reset_data'),
]