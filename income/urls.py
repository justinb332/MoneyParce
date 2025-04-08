from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_income, name='add_income'),
]