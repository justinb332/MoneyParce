import openai
from django.conf import settings
from reports.financial_ai import generate_financial_report
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from expense.models import Expense

openai.api_key = settings.OPENAI_API_KEY


def generate_financial_report(data):
    prompt = f"""
    You are a financial advisor. A user has the following data:
    - Income: ${data['income']}
    - Expenses: {data['expenses']}

     Based on this information:
    1. Provide a short summary of the financial situation.
    2. Offer 2-3 specific, actionable tips for improving budgeting or savings. Be polite and encouraging.
    """


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )

    return response['choices'][0]['message']['content']

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