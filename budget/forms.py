# forms.py (Budget app)

from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'amount', 'category', 'timeframe']
