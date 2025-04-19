from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_income, name='add_income'),
    path('edit/<slug:slug>/', views.edit_income, name='edit_income'),
    path('delete/<slug:slug>/', views.delete_income, name='delete-income'),

]