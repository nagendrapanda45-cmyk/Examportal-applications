# forms.py
from django import forms
from .models import EmailTemplate
from home.users.models import Configuration

class EmailTemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from datetime import datetime
        current_year = datetime.now().year  # Can be dynamic
        choices = [
            (config.value, config.value)
            for config in Configuration.objects.filter(
                key__startswith=f'email_template_{current_year}', deleted=False
            )
        ]
        self.fields['email_template'].choices = choices

    class Meta:
        model = EmailTemplate
        fields = ['email_template', 'subject', 'email_context']
        widgets = {
            'email_context': forms.HiddenInput(attrs={'id': 'email_context'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'email_template': forms.Select(attrs={'class': 'form-control'}),
        }
