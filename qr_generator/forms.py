from django import forms
from .models import QRGenerate

class QRGenerateForm(forms.ModelForm):
    class Meta:
        model = QRGenerate
        fields = ['name', 'target_url']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Name is required.")
        return name

    def clean_target_url(self):
        target_url = self.cleaned_data.get('target_url')
        if not target_url:
            raise forms.ValidationError("Target URL is required.")
        return target_url
