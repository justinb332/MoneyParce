from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from accounts.models import CustomUser
from income.models import Income
from transactions.models import Transaction

def home(request):
    transactions = Transaction.objects.all().order_by('-date')
    incomes = Income.objects.all().order_by('-date')
    return render(request, 'home/home.html', {'transactions': transactions, 'incomes': incomes})

def add_transaction(request):
    return render(request, 'transactions/add_transaction.html')

def add_income(request):
    return render(request, 'income/add_income.html')

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

@login_required
def reset_data(request):
    if request.method == 'POST':
        Income.objects.all().delete()
        Transaction.objects.all().delete()
        return redirect('settings')
    return redirect('settings')
