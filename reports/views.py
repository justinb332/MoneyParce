from openai import OpenAI
from django.conf import settings
from reports.financial_ai import generate_financial_report
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from expense.models import Expense

client = OpenAI(api_key=settings.OPENAI_API_KEY)

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
   report = create_report()
   return render(request, 'report.html', {'report': report})