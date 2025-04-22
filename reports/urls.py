from django.urls import path
from . import views
from .views import display_report

urlpatterns = [
    path('', display_report, name='reports'),
]