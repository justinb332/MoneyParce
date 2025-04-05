from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms

from accounts.models import CustomUser

CHOICES = [
        ('question1', "Question 1"),
        ('question2', "Question 2"),
        ('question3', "Question 3"),
    ]

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'security_question', 'security_answer')

    email = forms.EmailField()
    username = forms.CharField(min_length=6)
    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput)
    security_question = forms.ChoiceField(choices=CHOICES)
    security_answer = forms.CharField(min_length=4, max_length=64)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['security_question'].label = 'Security Question'
        self.fields['security_answer'].label = 'Security Answer'

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomPasswordResetForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ('username', 'security_question', 'security_answer')

    username = forms.CharField(min_length=6)
    new_password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    security_question = forms.ChoiceField(choices=CHOICES)
    security_answer = forms.CharField(min_length=4, max_length=64)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['new_password'].label = 'New Password'
        self.fields['security_question'].label = 'Security Question'
        self.fields['security_answer'].label = 'Security Answer'

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})