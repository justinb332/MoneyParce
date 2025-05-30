from openai import OpenAI
from django.conf import settings
import requests
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_financial_report(data):
    """
        Generates a financial report by sending request to OpenAI's API.

        Args:
            data (dict): A dictionary containing income and expense data.
                         Example format:
                         {
                             "income": [{"category": "Salary", "amount": 5000}],
                             "expenses": [{"category": "Rent", "amount": 2000}]
                         }

        Returns:
            str: The financial report text generated by OpenAI.
        """
    api_key = os.getenv("OPENAI_API_KEY") or openai.api_key  # Load API key from environment or global config

    if not api_key:
        raise ValueError("OpenAI API key is missing. Please set it as an environment variable.")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    DO NOT include ANY technical details. 
    Generate a financial summary report using the following data: {data}.
    The report should contain:
    1. Total Income and Total Expenses at the top.
    2. A breakdown of income and expenses using tables.
    3. A net balance calculation at the bottom.
    If there is a negative net balance, make it red.
    If there is a positive net balance, make it green.

    Format it all using clean HTML. Wrap tables with <table>, <tr>, <th>, and <td>. Ensure the layout is suited for a webpage.
    
    Provide a concise summary at the end.
    Included with the summary include a few financial tips listed out.
    DO NOT include ANY technical details. 
    Be positive and supportive.
    Double check your math.
    Center your report pretty please.
    """

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a financial reporting assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        # Extract the generated report from the response
        return data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        # Log the error and return a friendly error message
        return f"Failed to generate the report: {str(e)}"
    except KeyError:
        # Handles a scenario where the response is malformed or incomplete
        return "The response from OpenAI could not be parsed correctly."

