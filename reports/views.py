import os
import openai
from openai import OpenAI
from django.conf import settings
from reports.financial_ai import generate_financial_report
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from expense.models import Expense

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not set")

def create_report():
    # Fetch incomes and expenses for the given user
    incomes = Income.objects.all()
    expenses = Expense.objects.all()

    # Prepare data for the financial report
    income_data = [{'category': inc.category, 'amount': inc.amount} for inc in incomes]
    expense_data = [{'category': exp.category, 'amount': exp.amount} for exp in expenses]
    data = {'income': income_data, 'expenses': expense_data}

    # Generate the report using OpenAI
    report_text = generate_financial_report(data)

    # Save the report to your user's reports (Assuming you have a Report model)
    return report_text


@login_required
def display_report(request):
    """
    View to display the financial report to the user.
    """
    report = create_report()
    return render(request, 'reports/report.html', {'report': report})
