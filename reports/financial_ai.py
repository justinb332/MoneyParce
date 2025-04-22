import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def generate_financial_report(user_data):
    prompt = f"""
    You are a financial advisor. A user has the following data:
    - Income: ${user_data['income']:.2f}
    - Expenses: {user_data['expenses']}

    Provide a short summary of their financial situation and offer 2-3 specific, actionable tips to improve their budgeting or savings. Be polite and encouraging.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )

    return response['choices'][0]['message']['content']
