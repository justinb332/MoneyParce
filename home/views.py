import json
from datetime import date

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from accounts.models import CustomUser
from income.models import Income
from expense.models import Expense
from budget.models import Budget
from django.core.serializers.json import DjangoJSONEncoder


def home(request):
    if request.user.is_authenticated:
        expenses_qs = (Expense.objects
                       .filter(user=request.user)
                       .order_by('-date')
                       .values('amount', 'category__name', 'date'))

        incomes_qs = (Income.objects
                      .filter(user=request.user)
                      .order_by('-date')
                      .values('amount', 'category__name', 'date'))

        latest_expense = (Expense.objects
                          .filter(user=request.user)
                          .order_by('-date')
                          .first())

        latest_date = latest_expense.date.date() if latest_expense else None

    else:
        expenses_qs = []
        incomes_qs = []
        latest_date = None

    unique_expense_days = {e['date'].date() for e in expenses_qs}

    expenses = list(expenses_qs)
    incomes  = list(incomes_qs)
    for e in expenses:
        e['date'] = e['date'].strftime('%m-%d')
    for i in incomes:
        i['date'] = i['date'].strftime('%m-%d')

    num_unique_days = len(unique_expense_days)

    print(num_unique_days)
    context = {
        'expenses': json.dumps(expenses, cls=DjangoJSONEncoder),
        'incomes': json.dumps(incomes, cls=DjangoJSONEncoder),
        'incomes_raw': incomes,
        'num_days': num_unique_days,
        'has_expenses': len(expenses) > 0,
        'has_income': len(incomes) > 0,
        'latest_transaction_date': latest_date,
        'today_date': date.today(),
    }
    return render(request, 'home/home.html', context)

@login_required
def transactions_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    incomes  = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'home/transactions.html',
                  {'expenses': expenses, 'incomes': incomes})

@login_required
def add_expense(request):
    return render(request, 'expense/add_expense.html')

@login_required
def add_income(request):
    return render(request, 'income/add_income.html')

@login_required
def settings(request):
    return render(request, 'home/settings.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home'))
    return render(request, 'home/settings.html')

@login_required
def reset_data(request):
    if request.method == 'POST':
        Income.objects.filter(user=request.user).delete()
        Expense.objects.filter(user=request.user).delete()
        Budget.objects.filter(user=request.user).delete()
        return redirect('settings')
    return redirect('settings')
