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
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Mark fields as required
            self.fields['name'].required = True
            self.fields['amount'].required = True  # Make this required
            self.fields['catergory'].required = True # Ensure source is required
            self.fields['notes'].required = False
            self.fields['is_recurring'].required = False  # Optional field
            self.fields['recurrence_period'].required = False  # Optional
            self.fields['recurrence_day_of_week'].required = False  # Optional
            self.fields['recurrence_day_of_month'].required = False  # Optional