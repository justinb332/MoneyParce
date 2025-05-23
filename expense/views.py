from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from .models import Expense
from income.models import Income
from datetime import timedelta, datetime
from calendar import monthrange

def calculate_next_occurrence(current_date, period, day_of_week=None, day_of_month=None):
    today = current_date.date()

    if period == 'daily':
        return current_date + timedelta(days=1)

    elif period == 'weekly' and day_of_week:
        weekdays = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6,
        }
        target = weekdays.get(day_of_week.lower(), 0)
        days_ahead = (target - today.weekday() + 7) % 7
        if days_ahead == 0:
            days_ahead = 7
        return datetime.combine(today + timedelta(days=days_ahead), datetime.min.time())

    elif period == 'monthly' and day_of_month:
        year = today.year
        month = today.month + 1
        if month > 12:
            month = 1
            year += 1
        day = min(day_of_month, monthrange(year, month)[1])
        return datetime(year, month, day)

    return None

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user

            if not expense.date:
                expense.date = now()

            # copy cleaned-data extras
            expense.is_recurring = form.cleaned_data['is_recurring']
            expense.recurrence_period = form.cleaned_data['recurrence_period']
            expense.recurrence_day_of_week = form.cleaned_data['recurrence_day_of_week']
            expense.recurrence_day_of_month = form.cleaned_data['recurrence_day_of_month']

            if expense.is_recurring and expense.recurrence_period:
                expense.next_occurrence = calculate_next_occurrence(
                    now(),
                    expense.recurrence_period,
                    expense.recurrence_day_of_week,
                    expense.recurrence_day_of_month
                )

            expense.save()
            return redirect('transactions')
    else:
        form = ExpenseForm()

    return render(request, 'expense/add_expense.html', {'form': form})

@login_required
def edit_expense(request, slug):
    expense = get_object_or_404(Expense, slug=slug, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            updated = form.save(commit=False)
            # user stays the same (already set)
            updated.is_recurring              = form.cleaned_data['is_recurring']
            updated.recurrence_period         = form.cleaned_data['recurrence_period']
            updated.recurrence_day_of_week    = form.cleaned_data['recurrence_day_of_week']
            updated.recurrence_day_of_month   = form.cleaned_data['recurrence_day_of_month']

            if updated.is_recurring and updated.recurrence_period:
                updated.next_occurrence = calculate_next_occurrence(
                    now(), updated.recurrence_period,
                    updated.recurrence_day_of_week,
                    updated.recurrence_day_of_month
                )
            else:
                updated.next_occurrence = None

            updated.save()
            return redirect('transactions')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expense/edit_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, slug):
    expense = get_object_or_404(Expense, slug=slug, user=request.user)
    expense.delete()
    return redirect('transactions')

@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    incomes  = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'home/home.html', {'expenses': expenses,
                                              'incomes': incomes})
