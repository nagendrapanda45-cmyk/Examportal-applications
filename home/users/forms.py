from django import forms
# from .models import Candidate
from django.core.exceptions import ValidationError
from datetime import date
from .models import Candidate, Instruction,Configuration
import re
from datetime import date, datetime
from django.core.exceptions import ValidationError

import os
from datetime import datetime, timedelta

ALL_COUNTRY_CODES = [
    ('+93', '+93 (Afghanistan)'),
    ('+355', '+355 (Albania)'),
    ('+213', '+213 (Algeria)'),
    ('+1684', '+1684 (American Samoa)'),
    ('+376', '+376 (Andorra)'),
    ('+244', '+244 (Angola)'),
    ('+1264', '+1264 (Anguilla)'),
    ('+1268', '+1268 (Antigua and Barbuda)'),
    ('+54', '+54 (Argentina)'),
    ('+374', '+374 (Armenia)'),
    ('+297', '+297 (Aruba)'),
    ('+61', '+61 (Australia)'),
    ('+43', '+43 (Austria)'),
    ('+994', '+994 (Azerbaijan)'),
    ('+1242', '+1242 (Bahamas)'),
    ('+973', '+973 (Bahrain)'),
    ('+880', '+880 (Bangladesh)'),
    ('+1246', '+1246 (Barbados)'),
    ('+375', '+375 (Belarus)'),
    ('+32', '+32 (Belgium)'),
    ('+501', '+501 (Belize)'),
    ('+229', '+229 (Benin)'),
    ('+1441', '+1441 (Bermuda)'),
    ('+975', '+975 (Bhutan)'),
    ('+591', '+591 (Bolivia)'),
    ('+387', '+387 (Bosnia and Herzegovina)'),
    ('+267', '+267 (Botswana)'),
    ('+47', '+47 (Bouvet Island)'),
    ('+55', '+55 (Brazil)'),
    ('+246', '+246 (British Indian Ocean Territory)'),
    ('+1284', '+1284 (British Virgin Islands)'),
    ('+673', '+673 (Brunei)'),
    ('+359', '+359 (Bulgaria)'),
    ('+226', '+226 (Burkina Faso)'),
    ('+257', '+257 (Burundi)'),
    ('+855', '+855 (Cambodia)'),
    ('+237', '+237 (Cameroon)'),
    ('+1', '+1 (Canada)'),
    ('+238', '+238 (Cape Verde)'),
    ('+599', '+599 (Caribbean Netherlands)'),
    ('+1345', '+1345 (Cayman Islands)'),
    ('+236', '+236 (Central African Republic)'),
    ('+235', '+235 (Chad)'),
    ('+56', '+56 (Chile)'),
    ('+86', '+86 (China)'),
    ('+61', '+61 (Christmas Island)'),
    ('+61', '+61 (Cocos (Keeling) Islands)'),
    ('+57', '+57 (Colombia)'),
    ('+269', '+269 (Comoros)'),
    ('+242', '+242 (Congo)'),
    ('+682', '+682 (Cook Islands)'),
    ('+506', '+506 (Costa Rica)'),
    ('+385', '+385 (Croatia)'),
    ('+53', '+53 (Cuba)'),
    ('+599', '+599 (Curaçao)'),
    ('+357', '+357 (Cyprus)'),
    ('+420', '+420 (Czechia)'),
    ('+243', '+243 (DR Congo)'),
    ('+45', '+45 (Denmark)'),
    ('+253', '+253 (Djibouti)'),
    ('+1767', '+1767 (Dominica)'),
    ('+1', '+1 (Dominican Republic)'),
    ('+593', '+593 (Ecuador)'),
    ('+20', '+20 (Egypt)'),
    ('+503', '+503 (El Salvador)'),
    ('+240', '+240 (Equatorial Guinea)'),
    ('+291', '+291 (Eritrea)'),
    ('+372', '+372 (Estonia)'),
    ('+268', '+268 (Eswatini)'),
    ('+251', '+251 (Ethiopia)'),
    ('+500', '+500 (Falkland Islands)'),
    ('+298', '+298 (Faroe Islands)'),
    ('+679', '+679 (Fiji)'),
    ('+358', '+358 (Finland)'),
    ('+33', '+33 (France)'),
    ('+594', '+594 (French Guiana)'),
    ('+689', '+689 (French Polynesia)'),
    ('+262', '+262 (French Southern and Antarctic Lands)'),
    ('+241', '+241 (Gabon)'),
    ('+220', '+220 (Gambia)'),
    ('+995', '+995 (Georgia)'),
    ('+49', '+49 (Germany)'),
    ('+233', '+233 (Ghana)'),
    ('+350', '+350 (Gibraltar)'),
    ('+30', '+30 (Greece)'),
    ('+299', '+299 (Greenland)'),
    ('+1473', '+1473 (Grenada)'),
    ('+590', '+590 (Guadeloupe)'),
    ('+1671', '+1671 (Guam)'),
    ('+502', '+502 (Guatemala)'),
    ('+44', '+44 (Guernsey)'),
    ('+224', '+224 (Guinea)'),
    ('+245', '+245 (Guinea-Bissau)'),
    ('+592', '+592 (Guyana)'),
    ('+509', '+509 (Haiti)'),
    ('+504', '+504 (Honduras)'),
    ('+852', '+852 (Hong Kong)'),
    ('+36', '+36 (Hungary)'),
    ('+354', '+354 (Iceland)'),
    ('+91', '+91 (India)'),
    ('+62', '+62 (Indonesia)'),
    ('+98', '+98 (Iran)'),
    ('+964', '+964 (Iraq)'),
    ('+353', '+353 (Ireland)'),
    ('+44', '+44 (Isle of Man)'),
    ('+972', '+972 (Israel)'),
    ('+39', '+39 (Italy)'),
    ('+225', '+225 (Ivory Coast)'),
    ('+1876', '+1876 (Jamaica)'),
    ('+81', '+81 (Japan)'),
    ('+44', '+44 (Jersey)'),
    ('+962', '+962 (Jordan)'),
    ('+7', '+7 (Kazakhstan)'),
    ('+254', '+254 (Kenya)'),
    ('+686', '+686 (Kiribati)'),
    ('+383', '+383 (Kosovo)'),
    ('+965', '+965 (Kuwait)'),
    ('+996', '+996 (Kyrgyzstan)'),
    ('+856', '+856 (Laos)'),
    ('+371', '+371 (Latvia)'),
    ('+961', '+961 (Lebanon)'),
    ('+266', '+266 (Lesotho)'),
    ('+231', '+231 (Liberia)'),
    ('+218', '+218 (Libya)'),
    ('+423', '+423 (Liechtenstein)'),
    ('+370', '+370 (Lithuania)'),
    ('+352', '+352 (Luxembourg)'),
    ('+853', '+853 (Macau)'),
    ('+261', '+261 (Madagascar)'),
    ('+265', '+265 (Malawi)'),
    ('+60', '+60 (Malaysia)'),
    ('+960', '+960 (Maldives)'),
    ('+223', '+223 (Mali)'),
    ('+356', '+356 (Malta)'),
    ('+692', '+692 (Marshall Islands)'),
    ('+596', '+596 (Martinique)'),
    ('+222', '+222 (Mauritania)'),
    ('+230', '+230 (Mauritius)'),
    ('+262', '+262 (Mayotte)'),
    ('+52', '+52 (Mexico)'),
    ('+691', '+691 (Micronesia)'),
    ('+373', '+373 (Moldova)'),
    ('+377', '+377 (Monaco)'),
    ('+976', '+976 (Mongolia)'),
    ('+382', '+382 (Montenegro)'),
    ('+1664', '+1664 (Montserrat)'),
    ('+212', '+212 (Morocco)'),
    ('+258', '+258 (Mozambique)'),
    ('+95', '+95 (Myanmar)'),
    ('+264', '+264 (Namibia)'),
    ('+674', '+674 (Nauru)'),
    ('+977', '+977 (Nepal)'),
    ('+31', '+31 (Netherlands)'),
    ('+687', '+687 (New Caledonia)'),
    ('+64', '+64 (New Zealand)'),
    ('+505', '+505 (Nicaragua)'),
    ('+227', '+227 (Niger)'),
    ('+234', '+234 (Nigeria)'),
    ('+683', '+683 (Niue)'),
    ('+672', '+672 (Norfolk Island)'),
    ('+850', '+850 (North Korea)'),
    ('+389', '+389 (North Macedonia)'),
    ('+1670', '+1670 (Northern Mariana Islands)'),
    ('+47', '+47 (Norway)'),
    ('+968', '+968 (Oman)'),
    ('+92', '+92 (Pakistan)'),
    ('+680', '+680 (Palau)'),
    ('+970', '+970 (Palestine)'),
    ('+507', '+507 (Panama)'),
    ('+675', '+675 (Papua New Guinea)'),
    ('+595', '+595 (Paraguay)'),
    ('+51', '+51 (Peru)'),
    ('+63', '+63 (Philippines)'),
    ('+64', '+64 (Pitcairn Islands)'),
    ('+48', '+48 (Poland)'),
    ('+351', '+351 (Portugal)'),
    ('+1', '+1 (Puerto Rico)'),
    ('+974', '+974 (Qatar)'),
    ('+40', '+40 (Romania)'),
    ('+7', '+7 (Russia)'),
    ('+250', '+250 (Rwanda)'),
    ('+262', '+262 (Réunion)'),
    ('+590', '+590 (Saint Barthélemy)'),
    ('+2', '+2 (Saint Helena, Ascension and Tristan da Cunha)'),
    ('+1869', '+1869 (Saint Kitts and Nevis)'),
    ('+1758', '+1758 (Saint Lucia)'),
    ('+590', '+590 (Saint Martin)'),
    ('+508', '+508 (Saint Pierre and Miquelon)'),
    ('+1784', '+1784 (Saint Vincent and the Grenadines)'),
    ('+685', '+685 (Samoa)'),
    ('+378', '+378 (San Marino)'),
    ('+966', '+966 (Saudi Arabia)'),
    ('+221', '+221 (Senegal)'),
    ('+381', '+381 (Serbia)'),
    ('+248', '+248 (Seychelles)'),
    ('+232', '+232 (Sierra Leone)'),
    ('+65', '+65 (Singapore)'),
    ('+1721', '+1721 (Sint Maarten)'),
    ('+421', '+421 (Slovakia)'),
    ('+386', '+386 (Slovenia)'),
    ('+677', '+677 (Solomon Islands)'),
    ('+252', '+252 (Somalia)'),
    ('+27', '+27 (South Africa)'),
    ('+500', '+500 (South Georgia)'),
    ('+82', '+82 (South Korea)'),
    ('+211', '+211 (South Sudan)'),
    ('+34', '+34 (Spain)'),
    ('+94', '+94 (Sri Lanka)'),
    ('+249', '+249 (Sudan)'),
    ('+597', '+597 (Suriname)'),
    ('+4779', '+4779 (Svalbard and Jan Mayen)'),
    ('+46', '+46 (Sweden)'),
    ('+41', '+41 (Switzerland)'),
    ('+963', '+963 (Syria)'),
    ('+239', '+239 (São Tomé and Príncipe)'),
    ('+886', '+886 (Taiwan)'),
    ('+992', '+992 (Tajikistan)'),
    ('+255', '+255 (Tanzania)'),
    ('+66', '+66 (Thailand)'),
    ('+670', '+670 (Timor-Leste)'),
    ('+228', '+228 (Togo)'),
    ('+690', '+690 (Tokelau)'),
    ('+676', '+676 (Tonga)'),
    ('+1868', '+1868 (Trinidad and Tobago)'),
    ('+216', '+216 (Tunisia)'),
    ('+993', '+993 (Turkmenistan)'),
    ('+1649', '+1649 (Turks and Caicos Islands)'),
    ('+688', '+688 (Tuvalu)'),
    ('+90', '+90 (Türkiye)'),
    ('+256', '+256 (Uganda)'),
    ('+380', '+380 (Ukraine)'),
    ('+971', '+971 (United Arab Emirates)'),
    ('+44', '+44 (United Kingdom)'),
    ('+1', '+1 (United States)'),
    ('+268', '+268 (United States Minor Outlying Islands)'),
    ('+1340', '+1340 (United States Virgin Islands)'),
    ('+598', '+598 (Uruguay)'),
    ('+998', '+998 (Uzbekistan)'),
    ('+678', '+678 (Vanuatu)'),
    ('+3', '+3 (Vatican City)'),
    ('+58', '+58 (Venezuela)'),
    ('+84', '+84 (Vietnam)'),
    ('+681', '+681 (Wallis and Futuna)'),
    ('+2', '+2 (Western Sahara)'),
    ('+967', '+967 (Yemen)'),
    ('+260', '+260 (Zambia)'),
    ('+263', '+263 (Zimbabwe)'),
    ('+35818', '+35818 (Åland Islands)'),
]

current_year = datetime.now().year

class CandidateForm(forms.ModelForm):
    mobile_country_code = forms.ChoiceField(
        choices=ALL_COUNTRY_CODES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'max-width: 120px;'}),
    )
    alt_mobile_country_code = forms.ChoiceField(
        choices=ALL_COUNTRY_CODES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'max-width: 120px;'}),
    )

    # FIX: Explicitly define gender to add a placeholder
    gender = forms.ChoiceField(
        choices=[
            ('', 'Select the Gender'),
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    # FIX: Explicitly define primary_skills to add a placeholder
    primary_skills = forms.ChoiceField(
        choices=[('', 'Select your Primary Skills')] + Candidate.get_primary_skills_choices(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    class Meta:
        model = Candidate
        # ADDED 'user_confirmation_status' TO THE LIST BELOW TO FIX THE ERROR
        exclude = [
            'user_id', 'registration_id', 'uploaded_at', 'deleted', 'registered_at', 
            'password', 'is_active', 'is_staff', 'is_superuser', 'user_confirmation_status',
            'registration_rating', 'registration_feedback'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'gender': forms.Select(attrs={'class': 'form-control'}), # Now defined above
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'alternative_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            # 'primary_skills': forms.Select(attrs={'class': 'form-control'}), # Now defined above
            'other_skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'highest_qualification': forms.Select(attrs={'class': 'form-control'}),
            'specific_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'stream': forms.TextInput(attrs={'class': 'form-control'}),
            'college_or_university': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'highest_qualification_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'training_certification': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'certificate': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'id_proof': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
            'pan_no': forms.TextInput(attrs={'class': 'form-control'}),
            'reference': forms.Select(attrs={'class': 'form-control'}),
            'referred_by': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dob'].required = True
        self.fields['mobile'].required = True
        self.fields['pan_no'].required = True

        if self.instance and self.instance.pk:
            self.fields['photo'].required = False
            # self.fields['signature'].required = False
        else:
            self.fields['photo'].required = True
            # self.fields['signature'].required = True
            

    def clean_pan_no(self):
        pan = self.cleaned_data.get('pan_no')
        if not pan or not re.match(r'^[a-zA-Z0-9]{10}$', pan):
            raise ValidationError("PAN number must be exactly 10 alphanumeric characters.")
        if Candidate.objects.exclude(pk=self.instance.pk).filter(pan_no=pan).exists():
            raise ValidationError("Candidate with this PAN number already exists.")
        return pan

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\d{10}$', mobile):
            raise ValidationError("Mobile number must be exactly 10 digits.")
        # Check if mobile number already exists (excluding current instance)
        if self.instance and self.instance.pk:
            if Candidate.objects.exclude(pk=self.instance.pk).filter(mobile=mobile).exists():
                raise ValidationError("Candidate with this mobile number already exists.")
        else:
            if Candidate.objects.filter(mobile=mobile).exists():
                raise ValidationError("Candidate with this mobile number already exists.")
        return mobile

    def clean_alternative_mobile(self):
        alt_mobile = self.cleaned_data.get('alternative_mobile')
        if alt_mobile and (not alt_mobile.isdigit() or len(alt_mobile) != 10):
            raise ValidationError("Alternative mobile must be exactly 10 digits if provided.")
        return alt_mobile

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob:
            current_year = 2025
            age = current_year - dob.year
            # print(f"Calculated age: {age}")
            # print("age type:", type(age))
            if age < 18:
                raise ValidationError("User age must be  greater than 18 years")
        return dob

    def clean(self):
        cleaned_data = super().clean()
        
        # Validation for matching country codes if alternative mobile is provided
        alt_mobile = cleaned_data.get('alternative_mobile')
        if alt_mobile:
            mobile_cc = cleaned_data.get('mobile_country_code')
            alt_mobile_cc = cleaned_data.get('alt_mobile_country_code')
            if mobile_cc != alt_mobile_cc:
                raise ValidationError("The country code for your Alternative Mobile must match your Primary Mobile country code.")

        # Logic for primary_skills and other_skills
        primary_skills = cleaned_data.get('primary_skills')
        other_skills = cleaned_data.get('other_skills')

        if primary_skills == 'Others':
            if not other_skills:
                self.add_error('other_skills', 'This field is required when "Others" is selected for primary skills.')
        else:
            # If a different skill is selected, clear the other_skills field
            cleaned_data['other_skills'] = ''

        # Existing logic for reference
        reference = cleaned_data.get('reference')
        referred_by = cleaned_data.get('referred_by')
        if reference == 'Yes' and not referred_by:
            self.add_error('referred_by', 'This field is required when reference is Yes.')
            
        hq = cleaned_data.get('highest_qualification')
        percentage = cleaned_data.get('highest_qualification_percentage')
        cgpa = cleaned_data.get('cgpa')
        
        if hq in ['PG', 'PhD']:
            if cgpa is None:
                self.add_error('cgpa', 'This field is required for PG/PhD qualifications.')
            cleaned_data['highest_qualification_percentage'] = None
        elif hq:
            if percentage is None:
                self.add_error('highest_qualification_percentage', 'This field is required for this qualification.')
            cleaned_data['cgpa'] = None
        
        return cleaned_data
        
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            try:
                # Use filter().first() to avoid MultipleObjectsReturned
                config = Configuration.objects.filter(key=f'resume_max_size_mb_{current_year}').order_by('-updated_date').first()
                if not config:
                    raise Configuration.DoesNotExist
                max_size_mb = int(config.value)
            except (Configuration.DoesNotExist, ValueError):
                max_size_mb = 6  # Default fallback value
            ext = os.path.splitext(resume.name)[1].lower().strip()
            valid_extensions = ['.pdf', '.doc', '.docx']
            if ext not in valid_extensions:
                raise ValidationError("Only PDF and Word documents (.pdf, .doc, .docx) are allowed.")
            if resume.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Resume file size should not exceed {max_size_mb}MB.")
        return resume

    def clean_id_proof(self):
        id_proof = self.cleaned_data.get('id_proof')
        if id_proof:
            try:
                # FIX: Added f-string and used filter().first()
                config = Configuration.objects.filter(key=f'id_proof_max_size_kb_{current_year}').order_by('-updated_date').first()
                if not config:
                    raise Configuration.DoesNotExist
                max_size_kb = int(config.value)
            except (Configuration.DoesNotExist, ValueError):
                max_size_kb = 1024  # Default fallback value
            ext = os.path.splitext(id_proof.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
            if id_proof.size > max_size_kb * 1024:
                raise ValidationError(f"ID proof too large ( > {max_size_kb}KB )")
            if ext not in valid_extensions:
                raise ValidationError("ID proof must be a .jpg, .jpeg, .png, or .pdf file.")
        return id_proof

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            try:
                # Use filter().first() to avoid MultipleObjectsReturned
                config = Configuration.objects.filter(key=f'photo_max_size_kb_{current_year}').order_by('-updated_date').first()
                if not config:
                    raise Configuration.DoesNotExist
                max_size_kb = int(config.value)
            except (Configuration.DoesNotExist, ValueError):
                max_size_kb = 1024  # Default fallback value
            ext = os.path.splitext(photo.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if photo.size > max_size_kb * 1024:
                raise ValidationError(f"Photo too large ( > {max_size_kb}KB )")
            if ext not in valid_extensions:
                raise ValidationError("Photo must be a .jpg, .jpeg, or .png file.")
        return photo

    def clean_certificate(self):
        certificate = self.cleaned_data.get('certificate')
        if certificate:
            try:
                # Use filter().first() to avoid MultipleObjectsReturned
                config = Configuration.objects.filter(key=f'certificate_max_size_mb_{current_year}').order_by('-updated_date').first()
                if not config:
                    raise Configuration.DoesNotExist
                max_size_mb = int(config.value)
            except (Configuration.DoesNotExist, ValueError):
                max_size_mb = 6  # Default fallback value
            ext = os.path.splitext(certificate.name)[1].lower().strip()
            valid_extensions = ['.pdf', '.doc', '.docx']
            if ext not in valid_extensions:
                raise ValidationError("Only PDF and Word documents (.pdf, .doc, .docx) are allowed.")
            if certificate.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Certificate file size should not exceed {max_size_mb}MB.")
        return certificate

class CandidateRegistrationForm(forms.ModelForm):
    mobile_country_code = forms.ChoiceField(
        choices=ALL_COUNTRY_CODES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'max-width: 120px;'}),
    )
    alt_mobile_country_code = forms.ChoiceField(
        choices=ALL_COUNTRY_CODES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'max-width: 120px;'}),
    )

    other_skills = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Specify other skills'
        }),
        required=False
    )

    # Override gender field to set custom empty_label
    gender = forms.ChoiceField(
        choices=[
            ('', 'Select the Gender'),
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    # Override primary_skills field to include empty choice
    primary_skills = forms.ChoiceField(
        choices=[('', 'Select your Primary Skills')] + Candidate.get_primary_skills_choices(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super(CandidateRegistrationForm, self).__init__(*args, **kwargs)
        # Set the max attribute for the dob field to today's date to disable future dates
        self.fields['dob'].widget.attrs['max'] = date.today().strftime('%Y-%m-%d')

    class Meta:
        model = Candidate
        fields = [
            'first_name', 'last_name', 'gender', 'dob', 'email', 'mobile_country_code', 'mobile',
            'alt_mobile_country_code', 'alternative_mobile', 'address', 'city', 'pincode', 'primary_skills',
            'other_skills', 'highest_qualification', 'specific_qualification', 'stream',
            'college_or_university', 'highest_qualification_percentage', 'cgpa', 'training_certification', 'certificate',
            'photo', 'resume', 'id_proof', 'pan_no', 'reference', 'referred_by'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'dob': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-digit mobile number'
            }),
            'alternative_mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter alternative mobile (optional)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter full address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter pincode'
            }),
            'highest_qualification': forms.Select(attrs={'class': 'form-control'}),
            'specific_qualification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., B.Tech, MBA, etc.'
            }),
            'stream': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Computer Science, Commerce, etc.'
            }),
            'college_or_university': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter college/university name'
            }),
            'highest_qualification_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter percentage (e.g., 85.50)',
                'step': '0.01'
            }),
            'cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter CGPA (e.g., 8.5)',
                'step': '0.01'
            }),
            'training_certification': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List any training or certifications (optional)'
            }),
            'certificate': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'id_proof': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'pan_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-character PAN number'
            }),
            'reference': forms.Select(attrs={'class': 'form-control'}),
            'referred_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter referrer name'
            }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-Z\s]+$', first_name):
            raise ValidationError("First name should contain only alphabets and spaces.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not re.match(r'^[a-zA-Z\s]+$', last_name):
            raise ValidationError("Last name should contain only alphabets and spaces.")
        return last_name

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\d{10}$', mobile):
            raise ValidationError("Mobile number must be exactly 10 digits.")
        if self.instance and self.instance.pk:
            if Candidate.objects.exclude(pk=self.instance.pk).filter(mobile=mobile).exists():
                raise ValidationError("Candidate with this mobile number already exists.")
        else:
            if Candidate.objects.filter(mobile=mobile).exists():
                raise ValidationError("Candidate with this mobile number already exists.")
        return mobile

    def clean_alternative_mobile(self):
        alt_mobile = self.cleaned_data.get('alternative_mobile')
        if alt_mobile and not re.match(r'^\d{10}$', alt_mobile):
            raise ValidationError("Alternative mobile number must be exactly 10 digits.")
        return alt_mobile

    def clean_pan_no(self):
        pan = self.cleaned_data.get('pan_no')
        if not pan or not re.match(r'^[a-zA-Z0-9]{10}$', pan):
            raise ValidationError("PAN number must be exactly 10 alphanumeric characters.")
        if Candidate.objects.exclude(pk=self.instance.pk).filter(pan_no=pan).exists():
            raise ValidationError("Candidate with this PAN number already exists.")
        return pan

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise ValidationError("You must be at least 18 years old to register.")
            if dob > today:
                raise ValidationError("Date of birth cannot be in the future.")
        return dob

    def clean_highest_qualification_percentage(self):
        percentage = self.cleaned_data.get('highest_qualification_percentage')
        if percentage is not None and (percentage < 0 or percentage > 100):
            raise ValidationError("Percentage must be between 0 and 100.")
        return percentage

    def clean_cgpa(self):
        cgpa = self.cleaned_data.get('cgpa')
        if cgpa is not None and (cgpa < 0 or cgpa > 10):
            raise ValidationError("CGPA must be between 0 and 10.")
        return cgpa

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            try:
                config = Configuration.objects.filter(key=f'resume_max_size_mb_{current_year}').order_by('-updated_date').first()
                if not config:
                    raise Configuration.DoesNotExist
                max_size_mb = int(config.value)
            except (Configuration.DoesNotExist, ValueError):
                max_size_mb = 6
            ext = os.path.splitext(resume.name)[1].lower().strip()
            valid_extensions = ['.pdf', '.doc', '.docx']
            if ext not in valid_extensions:
                raise ValidationError("Only PDF and Word documents (.pdf, .doc, .docx) are allowed.")
            if resume.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Resume file size should not exceed {max_size_mb}MB.")
        return resume

    def clean_id_proof(self):
        id_proof = self.cleaned_data.get('id_proof')
        if id_proof:
            try:
                config = Configuration.objects.filter(key=f'id_proof_max_size_kb_{current_year}').order_by('-updated_date').first()
                if not config:
                    raise Configuration.DoesNotExist
                max_size_kb = int(config.value)
            except (Configuration.DoesNotExist, ValueError):
                max_size_kb = 1024
            ext = os.path.splitext(id_proof.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
            if id_proof.size > max_size_kb * 1024:
                raise ValidationError(f"ID proof too large ( > {max_size_kb}KB )")
            if ext not in valid_extensions:
                raise ValidationError("ID proof must be a .jpg, .jpeg, .png, or .pdf file.")
        return id_proof

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            try:
                config = Configuration.objects.filter(key=f'photo_max_size_kb_{current_year}').order_by('-updated_date').first()
                if not config:
                    raise Configuration.DoesNotExist
                max_size_kb = int(config.value)
            except (Configuration.DoesNotExist, ValueError):
                max_size_kb = 1024
            ext = os.path.splitext(photo.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if photo.size > max_size_kb * 1024:
                raise ValidationError(f"Photo too large ( > {max_size_kb}KB )")
            if ext not in valid_extensions:
                raise ValidationError("Photo must be a .jpg, .jpeg, or .png file.")
        return photo

    def clean_certificate(self):
        certificate = self.cleaned_data.get('certificate')
        if certificate:
            try:
                config = Configuration.objects.filter(key=f'certificate_max_size_mb_{current_year}').order_by('-updated_date').first()
                if not config:
                    raise Configuration.DoesNotExist
                max_size_mb = int(config.value)
            except (Configuration.DoesNotExist, ValueError):
                max_size_mb = 6
            ext = os.path.splitext(certificate.name)[1].lower().strip()
            valid_extensions = ['.pdf', '.doc', '.docx']
            if ext not in valid_extensions:
                raise ValidationError("Only PDF and Word documents (.pdf, .doc, .docx) are allowed.")
            if certificate.size > max_size_mb * 1024 * 1024:
                raise ValidationError(f"Certificate file size should not exceed {max_size_mb}MB.")
        return certificate

    def clean_primary_skills(self):
        primary_skills = self.cleaned_data.get('primary_skills')
        valid_skills = [skill[0] for skill in Candidate.get_primary_skills_choices()]
        if primary_skills not in valid_skills:
            raise ValidationError("Please select a valid primary skill.")
        return primary_skills
    
    def clean(self):
        cleaned_data = super().clean()

        # Validation for matching country codes if alternative mobile is provided
        alt_mobile = cleaned_data.get('alternative_mobile')
        if alt_mobile:
            mobile_cc = cleaned_data.get('mobile_country_code')
            alt_mobile_cc = cleaned_data.get('alt_mobile_country_code')
            if mobile_cc != alt_mobile_cc:
                raise ValidationError("The country code for your Alternative Mobile must match your Primary Mobile country code.")

        # Password validation removed
        
        reference = cleaned_data.get('reference')
        referred_by = cleaned_data.get('referred_by')
        
        if reference == 'Yes' and not referred_by:
            raise ValidationError("Please provide the referrer's name.")
            
        hq = cleaned_data.get('highest_qualification')
        percentage = cleaned_data.get('highest_qualification_percentage')
        cgpa = cleaned_data.get('cgpa')
        
        if hq in ['PG', 'PhD']:
            if cgpa is None:
                self.add_error('cgpa', 'This field is required for PG/PhD qualifications.')
            cleaned_data['highest_qualification_percentage'] = None
        elif hq:
            if percentage is None:
                self.add_error('highest_qualification_percentage', 'This field is required for this qualification.')
            cleaned_data['cgpa'] = None
        
        return cleaned_data
    

class UserLoginForm(forms.Form):
    registration_id = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'REG-YYYY-DOB-INTITIN000001'
        })
    )
    
    dob = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        registration_id = cleaned_data.get('registration_id')
        dob = cleaned_data.get('dob')
        
        if registration_id and dob:
            try:
                user = Candidate.objects.get(
                    registration_id=registration_id,
                    dob=dob,
                    is_active=True,
                    deleted=False
                )
                cleaned_data['user'] = user
            except Candidate.DoesNotExist:
                raise ValidationError("Invalid registration ID or date of birth.")
        
        return cleaned_data
    

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = [
            'test_name', 'test_type', 'title', 'content', 
            'display_order', 'is_active'
        ]
        
        widgets = {
            'test_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter test name (e.g., General Test, Technical Test)'
            }),
            'test_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter instruction title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Enter instruction content (HTML or plain text)'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter display order (0 for first)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_display_order(self):
        display_order = self.cleaned_data.get('display_order')
        if display_order is not None and display_order < 0:
            raise ValidationError("Display order cannot be negative.")
        return display_order