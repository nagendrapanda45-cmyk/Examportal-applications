from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Employee

class EmployeeForm(UserCreationForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter full name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )
    department = forms.ChoiceField(
        choices=[
            ('Programming Team', 'Programming Team'),
            ('Recruiter', 'Recruiter'),
            ('Human Resources (HR)', 'Human Resources (HR)'),
            ('Finance', 'Finance'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'department', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id if self.instance else None).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = True
        if commit:
            user.save()
            Employee.objects.update_or_create(
                user=user,
                defaults={
                    'name': self.cleaned_data['name'],
                    'email': self.cleaned_data['email'],
                    'department': self.cleaned_data['department']
                }
            )
        return user

class EmployeeEditForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter full name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username cannot be changed',
            'readonly': 'readonly',
            'disabled': 'disabled'
        })
    )
    department = forms.ChoiceField(
        choices=[
            ('Programming Team', 'Programming Team'),
            ('Recruiter', 'Recruiter'),
            ('Human Resources (HR)', 'Human Resources (HR)'),
            ('Finance', 'Finance'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Employee
        fields = ('name', 'email', 'department')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['username'].initial = self.instance.user.username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Employee.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def save(self, commit=True):
        employee = super().save(commit=False)
        user = employee.user
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            employee.save()
        return employee