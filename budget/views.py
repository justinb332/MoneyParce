# views.py (Budget app)

from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Budget
from .forms import BudgetForm
from budget.utils.budget_manager import BudgetManager

def budget_list(request):
    manager = BudgetManager()
    budget_data = manager.get_budget_summaries(request.user)

    return render(request, 'budget/budget_list.html', {'budget_data': budget_data})

def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            try:
                budget = form.save(commit=False)  # Don't save to DB yet
                budget.user = request.user        # Attach the logged-in user
                budget.save()                     # Now save it
                return redirect('budget_list')
            except IntegrityError:
                form.add_error(None, "A budget with this category and timeframe already exists.")
    else:
        form = BudgetForm()

    return render(request, 'budget/add_budget.html', {'form': form})

def edit_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            try:
                form.save()
                return redirect('budget_list')
            except IntegrityError:
                form.add_error(None, "A budget with this category and timeframe already exists.")
    else:
        form = BudgetForm(instance=budget)

    return render(request, 'budget/edit_budget.html', {'form': form})

def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    budget.delete()  # Delete the budget from the database
    return redirect('budget_list')  # Redirect to the budget list page
