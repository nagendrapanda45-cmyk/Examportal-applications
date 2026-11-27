import re

with open('home/users/forms.py', 'r') as f:
    content = f.read()

choices_str = '''
    mobile_country_code = forms.ChoiceField(
        choices=[('+91', '+91 (IND)'), ('+1', '+1 (USA/CAN)'), ('+44', '+44 (UK)'), ('+61', '+61 (AUS)')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'max-width: 120px;'}),
    )
    alt_mobile_country_code = forms.ChoiceField(
        choices=[('+91', '+91 (IND)'), ('+1', '+1 (USA/CAN)'), ('+44', '+44 (UK)'), ('+61', '+61 (AUS)')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'max-width: 120px;'}),
    )
'''

content = re.sub(r'(class CandidateForm\(forms\.ModelForm\):)', r'\g<1>' + choices_str, content)
content = re.sub(r'(class CandidateRegistrationForm\(forms\.ModelForm\):)', r'\g<1>' + choices_str, content)

content = content.replace("'email', 'mobile',", "'email', 'mobile_country_code', 'mobile',")
content = content.replace("'alternative_mobile',", "'alt_mobile_country_code', 'alternative_mobile',")

with open('home/users/forms.py', 'w') as f:
    f.write(content)
