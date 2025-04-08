from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Income
from .forms import IncomeForm

# Create your views here.
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IncomeForm()
    return render(request, 'income/add_income.html', {'form': form})

def edit_income(request, name):
    income = get_object_or_404(Income, name=name)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('home')  # Adjust the redirect as necessary
    else:
        form = IncomeForm(instance=income)
    return render(request, 'income/edit_income.html', {'form': form})

def delete_income(request, name):
    income = get_object_or_404(Income, name=name)
    income.delete()
    return redirect('home')


def home(request):
    incomes = Income.objects.all().order_by('-date')
    return render(request, 'home/home.html', {'incomes': incomes})

