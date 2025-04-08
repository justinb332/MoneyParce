from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_income, name='add_income'),
    path('edit/<str:name>/', views.edit_income, name='edit_income'),
]