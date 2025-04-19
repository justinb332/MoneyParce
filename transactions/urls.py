from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<slug:slug>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<slug:slug>/', views.delete_transaction, name='delete-transaction'),

]
