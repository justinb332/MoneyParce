from django.urls import path
from . import views


urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('display/', views.display_report, name='reports_display'),
]