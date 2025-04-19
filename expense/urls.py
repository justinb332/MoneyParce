from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<slug:slug>/', views.edit_expense, name='edit_expense'),
    path('delete/<slug:slug>/', views.delete_expense, name='delete_expense'),

]
