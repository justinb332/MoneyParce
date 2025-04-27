from django import forms
from .models import Budget
from expense.models import Category


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'total_amount']  # Fields to include in the form
        widgets = {
            'category': forms.Select(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].disabled = True  # Disable category field (read-only, pre-filled)
