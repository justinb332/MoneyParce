from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)



def generate_financial_report(user_data):
    # Calculate total income and expenses
    total_income = sum(item.get('amount', 0) for item in user_data.get('income', []))
    total_expenses = sum(item.get('amount', 0) for item in user_data.get('expenses', []))

    # Construct the prompt
    prompt = f"""
        You are a financial advisor. A user has the following data:
        - Income: ${total_income:.2f}
        - Expenses: ${total_expenses:.2f}

        Provide a short summary of their financial situation and offer 2-3 specific, actionable tips to improve their budgeting or savings. Be polite and encouraging.
        """

    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content

