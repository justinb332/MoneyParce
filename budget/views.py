# views.py (Budget app)

from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Budget
from .forms import BudgetForm

def budget_list(request):
    # Get all budget and order by timeframe (daily first, weekly second, monthly last)
    budgets = Budget.objects.all().order_by("timeframe")

    # Precompute the total spent for each budget for today, this week, or this month
    budget_data = []
    for budget in budgets:
        total_spent = None

        if budget.timeframe == 'daily':
            total_spent = budget.total_spent('daily')
        elif budget.timeframe == 'weekly':
            total_spent = budget.total_spent('weekly')
        elif budget.timeframe == 'monthly':
            total_spent = budget.total_spent('monthly')

        total_spent = budget.total_spent(budget.timeframe)
        remaining_amount = budget.amount - total_spent
        over_budget = None

        # Check if the budget is over
        if total_spent > budget.amount:
            over_budget = total_spent - budget.amount

        # Add to each budget object
        budget.remaining_amount = remaining_amount
        budget.over_budget = over_budget

        budget_data.append({
            'budget': budget,
            'total_spent': total_spent,
        })

    return render(request, 'budget/budget_list.html', {'budget_data': budget_data})

def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            try:
                form.save()
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
