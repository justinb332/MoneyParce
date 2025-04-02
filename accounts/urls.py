from django.urls import path
from . import views
from .views import logout_view, CustomLoginView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
]