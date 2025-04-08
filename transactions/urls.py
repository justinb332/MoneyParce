from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<str:name>/', views.edit_transaction, name='edit_transaction'),
]
