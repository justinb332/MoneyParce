import os
import openai
from reports.financial_ai import generate_financial_report
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from expense.models import Expense
from django import forms


openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not set")

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))


def reports_home(request):
    form = DateRangeForm()

    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            # Get the cleaned data from the form
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Logic for handling the selected date range
            return display_report(request, start_date, end_date)

    return render(request, 'reports/home.html', {'form': form})



@login_required
def display_report(request, start_date, end_date):
    """
    View to display the financial report to the user.
    """
    if start_date != None or end_date != None:
        incomes = Income.objects.filter(date__range=(start_date, end_date))
        expenses = Expense.objects.filter(date__range=(start_date, end_date))
    # Fetch incomes and expenses for the given user
    else:
        incomes = Income.objects.all()
        expenses = Expense.objects.all()

    # Prepare data for the financial report
    income_data = [{'category': inc.category, 'amount': inc.amount} for inc in incomes]
    expense_data = [{'category': exp.category, 'amount': exp.amount} for exp in expenses]
    data = {'income': income_data, 'expenses': expense_data}

    report = generate_financial_report(data)
    return render(request, 'reports/results.html', {'report': report})
