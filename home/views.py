import json
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from accounts.models import CustomUser
from income.models import Income
from expense.models import Expense
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date

def home(request):
    expenses = list(Expense.objects.all().order_by('-date').values('amount', 'category__name', 'date'))
    incomes = list(Income.objects.all().order_by('-date').values('amount', 'category__name', 'date'))

    latest_expense = Expense.objects.latest('date')
    latest_transaction_date = latest_expense.date.date()
    today_date = date.today()

    # Formatting
    for expense in expenses:
        expense['date'] = expense['date'].strftime('%m-%d')
    for income in incomes:
        income['date'] = income['date'].strftime('%m-%d')
    expenses_json = json.dumps(expenses, cls=DjangoJSONEncoder)
    incomes_json = json.dumps(incomes, cls=DjangoJSONEncoder)

    return render(request, 'home/home.html', {
        'expenses': expenses_json,
        'incomes': incomes_json,
        'latest_transaction_date': latest_transaction_date,
        'today_date': today_date,
    })

def transactions_view(request):
    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    context = {'expenses': expenses, 'incomes': incomes}
    return render(request, 'home/transactions.html', context)

def add_expense(request):
    return render(request, 'expense/add_expense.html')

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
        Expense.objects.all().delete()
        return redirect('settings')
    return redirect('settings')
