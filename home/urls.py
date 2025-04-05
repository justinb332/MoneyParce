from django.urls import path
from .views import home, add_transaction

urlpatterns = [
    path('', home, name='home'),
    path('transactions/', add_transaction, name='add_transaction'),
]