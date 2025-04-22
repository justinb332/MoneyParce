from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'name', 'amount', 'category', 'notes',
            'is_recurring', 'recurrence_period',
            'recurrence_day_of_week', 'recurrence_day_of_month'
        ]