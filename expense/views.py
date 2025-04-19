from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from income.models import Income
from .forms import ExpenseForm
from .models import Expense


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    else:
        form = ExpenseForm()

    return render(request, 'expense/add_expense.html', {'form': form})

def edit_expense(request, slug):
    expense = get_object_or_404(Expense, slug=slug)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('home')  # Adjust the redirect as necessary
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense/edit_expense.html', {'form': form})

def delete_expense(request, slug):
    expense = get_object_or_404(Expense, slug=slug)
    expense.delete()
    return redirect('home')


def home(request):
    expenses = Expense.objects.all().order_by('-date')
    incomes = Income.objects.all().order_by('-date')
    return render(request, 'home/home.html', {'expenses': expenses, 'incomes': incomes})