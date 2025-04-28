from django import forms


class ReportForm(forms.Form):
    start_date = forms.DateField(required=False)  # Make fields optional
    end_date = forms.DateField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Check if only one of the dates is filled
        if (start_date and not end_date) or (not start_date and end_date):
            raise forms.ValidationError('Please fill in both start and end dates or leave them blank.')

        return cleaned_data