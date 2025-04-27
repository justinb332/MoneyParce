from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from income.models import Income
from expense.models import Expense, Category
from .models import Budget
from .forms import BudgetForm
from django.forms import modelformset_factory


@login_required
def budget_page(request):
    """
    View to manage budgets for all expense categories at once.
    """
    # Ensure every category has an associated budget (initialize missing budgets)
    for category in Category.objects.all():
        Budget.objects.get_or_create(category=category, defaults={'total_amount': 0})

    # Create a formset for managing budgets
    BudgetFormSet = modelformset_factory(Budget, fields=['category', 'total_amount'], extra=0)

    if request.method == 'POST':
        formset = BudgetFormSet(request.POST)
        if formset.is_valid():
            formset.save()  # Save all submitted budgets
            return redirect('budget_page')  # Redirect to the same page after saving

    else:
        formset = BudgetFormSet(queryset=Budget.objects.select_related('category'))


    # Fetch existing budgets and calculate spent amounts per category
    budgets = Budget.objects.all()
    expenses = Category.objects.prefetch_related('expense_set')  # Related expenses for each category
    category_spending = {category: sum(e.amount for e in category.expense_set.all()) for category in expenses}

    context = {
        'formset': formset,  # Pass the formset to the template
        'budgets': budgets,  # All budgets
        'category_spending': category_spending,  # Spending per category
    }

    return render(request, 'budget/budget.html', context)