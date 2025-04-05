from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.core.exceptions import ValidationError

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
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email already registered')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        return password2

    def clean(self):
        form_data = self.cleaned_data
        if form_data['password1'] != form_data['password2']:
            self._errors['password1'] = ["Passwords don't match"]
            del form_data['password1']
            del form_data['password2']
        return form_data

class CustomPasswordResetForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ('username', 'security_question', 'security_answer')

    username = forms.CharField(min_length=6)
    new_password1 = forms.CharField(min_length=8, widget=forms.PasswordInput)
    new_password2 = forms.CharField(min_length=8, widget=forms.PasswordInput)
    security_question = forms.ChoiceField(choices=CHOICES)
    security_answer = forms.CharField(min_length=4, max_length=64)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm New Password'
        self.fields['security_question'].label = 'Security Question'
        self.fields['security_answer'].label = 'Security Answer'

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data['username']
        if not CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Username doesn\'t exist')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        return password2

    def clean(self):
        form_data = self.cleaned_data
        user = CustomUser.objects.get(username=form_data['username']) #figure out if i need to check if username is valid?
        if form_data['new_password1'] == form_data['new_password2']:
            if not user.check_password(form_data['new_password1']):
                if user.security_question == form_data['security_question']:
                    if user.security_answer == form_data['security_answer']:
                        return form_data
                else:
                    self._errors['security_answer'] = ["Security question or answer doesn't match"]
                    del form_data['security_question']
                    del form_data['security_answer']
            else:
                self._errors['new_password1'] = ["New password must not match old password"]
                del form_data['new_password1']
                del form_data['new_password2']
        else:
            self._errors['new_password1'] = ["Passwords don't match"]
            del form_data['new_password1']
            del form_data['new_password2']