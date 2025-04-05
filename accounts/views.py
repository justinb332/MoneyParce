from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

from accounts.forms import SignUpForm, CustomPasswordResetForm
from accounts.models import CustomUser

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

def reset_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            return redirect('login')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'accounts/reset.html', {'form': form})