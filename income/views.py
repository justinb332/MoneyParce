from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm
from .models import Income
from datetime import timedelta, datetime
from calendar import monthrange

def calculate_next_occurrence(current_date, period, day_of_week=None, day_of_month=None):
    today = now().date()

    if period == 'daily':
        return now() + timedelta(days=1)

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
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user

            if not income.date:
                income.date = now()

            # copy recurring-data fields
            income.is_recurring            = form.cleaned_data['is_recurring']
            income.recurrence_period       = form.cleaned_data['recurrence_period']
            income.recurrence_day_of_week  = form.cleaned_data['recurrence_day_of_week']
            income.recurrence_day_of_month = form.cleaned_data['recurrence_day_of_month']

            # compute next_occurrence
            if income.is_recurring and income.recurrence_period:
                income.next_occurrence = calculate_next_occurrence(
                    now(), income.recurrence_period,
                    income.recurrence_day_of_week,
                    income.recurrence_day_of_month
                )

            income.save()
            return redirect('transactions')
    else:
        form = IncomeForm()

    return render(request, 'income/add_income.html', {'form': form})

@login_required
def edit_income(request, slug):
    # only let the owner retrieve this income
    income = get_object_or_404(Income, slug=slug, user=request.user)

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            updated = form.save(commit=False)
            # user stays unchanged (still request.user)

            updated.is_recurring            = form.cleaned_data['is_recurring']
            updated.recurrence_period       = form.cleaned_data['recurrence_period']
            updated.recurrence_day_of_week  = form.cleaned_data['recurrence_day_of_week']
            updated.recurrence_day_of_month = form.cleaned_data['recurrence_day_of_month']

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
        form = IncomeForm(instance=income)

    return render(request, 'income/edit_income.html',
                  {'form': form, 'income': income})


@login_required
def delete_income(request, slug):
    income = get_object_or_404(Income, slug=slug, user=request.user)
    income.delete()
    return redirect('transactions')

@login_required
def home(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'home/home.html', {'incomes': incomes})
