from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from accounts.models import CustomUser
from transactions.models import Transaction

def home(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'home/home.html', {'transactions': transactions})

def add_transaction(request):
    return render(request, 'transactions/add_transaction.html')

@login_required
def settings(request):
    return render(request, 'home/settings.html')

@login_required
def delete_account(request):
    user = CustomUser.objects.get(username=request.user)
    if request.method == 'POST':
        CustomUser.objects.get(username=user).delete()
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home'))
    return render(request, 'home/settings.html')