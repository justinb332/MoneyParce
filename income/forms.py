from django import forms
from .models import Income

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = [
            'name', 'amount', 'category', 'notes',
            'is_recurring', 'recurrence_period',
            'recurrence_day_of_week', 'recurrence_day_of_month'
        ]

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        # Mark fields as required
        self.fields['name'].required = True
        self.fields['amount'].required = True  # Make this required
        self.fields['category'].required = True # Ensure source is required
        self.fields['category'].queryset = Category.objects.all()
        self.fields['notes'].required = False
        self.fields['is_recurring'].required = False  # Optional field
        self.fields['recurrence_period'].required = False  # Optional
        self.fields['recurrence_day_of_week'].required = False  # Optional
        self.fields['recurrence_day_of_month'].required = False  # Optional

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['is_recurring'].widget.attrs['class'] = 'form-check-label'