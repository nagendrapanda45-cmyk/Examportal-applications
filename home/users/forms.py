from django import forms
# from .models import Users
from django.core.exceptions import ValidationError
from datetime import date
from .models import Users, Instruction,Configuration
import re
from datetime import date, datetime
from django.core.exceptions import ValidationError

import os
from datetime import datetime, timedelta

current_year = datetime.now().year

class UsersForm(forms.ModelForm):
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
        choices=[('', 'Select your Primary Skills')] + Users.get_primary_skills_choices(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    class Meta:
        model = Users
        # ADDED 'user_confirmation_status' TO THE LIST BELOW TO FIX THE ERROR
        exclude = [
            'user_id', 'registration_id', 'uploaded_at', 'deleted', 'registered_at', 
            'password', 'is_active', 'is_staff', 'is_superuser', 'user_confirmation_status'
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
            'aadhar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'reference': forms.Select(attrs={'class': 'form-control'}),
            'referred_by': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dob'].required = True
        self.fields['mobile'].required = True
        self.fields['aadhar_number'].required = True

        if self.instance and self.instance.pk:
            self.fields['photo'].required = False
            # self.fields['signature'].required = False
        else:
            self.fields['photo'].required = True
            # self.fields['signature'].required = True
            

    def clean_aadhar_number(self):
        aadhar = self.cleaned_data.get('aadhar_number')
        if not aadhar.isdigit() or len(aadhar) != 12:
            raise ValidationError("Aadhar number must be exactly 12 digits.")
        if Users.objects.exclude(pk=self.instance.pk).filter(aadhar_number=aadhar).exists():
            raise ValidationError("Users with this Aadhar number already exists..")
        return aadhar

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\d{10}$', mobile):
            raise ValidationError("Mobile number must be exactly 10 digits.")
        # Check if mobile number already exists (excluding current instance)
        if self.instance and self.instance.pk:
            if Users.objects.exclude(pk=self.instance.pk).filter(mobile=mobile).exists():
                raise ValidationError("Users with this mobile number already exists.")
        else:
            if Users.objects.filter(mobile=mobile).exists():
                raise ValidationError("Users with this mobile number already exists.")
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

class UserRegistrationForm(forms.ModelForm):
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
        choices=[('', 'Select your Primary Skills')] + Users.get_primary_skills_choices(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Set the max attribute for the dob field to today's date to disable future dates
        self.fields['dob'].widget.attrs['max'] = date.today().strftime('%Y-%m-%d')

    class Meta:
        model = Users
        fields = [
            'first_name', 'last_name', 'gender', 'dob', 'email', 'mobile',
            'alternative_mobile', 'address', 'city', 'pincode', 'primary_skills',
            'other_skills', 'highest_qualification', 'specific_qualification', 'stream',
            'college_or_university', 'highest_qualification_percentage', 'cgpa', 'training_certification', 'certificate',
            'photo', 'resume', 'id_proof', 'aadhar_number', 'reference', 'referred_by'
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
            'aadhar_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 12-digit Aadhar number'
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
            if Users.objects.exclude(pk=self.instance.pk).filter(mobile=mobile).exists():
                raise ValidationError("Users with this mobile number already exists.")
        else:
            if Users.objects.filter(mobile=mobile).exists():
                raise ValidationError("Users with this mobile number already exists.")
        return mobile

    def clean_alternative_mobile(self):
        alt_mobile = self.cleaned_data.get('alternative_mobile')
        if alt_mobile and not re.match(r'^\d{10}$', alt_mobile):
            raise ValidationError("Alternative mobile number must be exactly 10 digits.")
        return alt_mobile

    def clean_aadhar_number(self):
        aadhar = self.cleaned_data.get('aadhar_number')
        if not aadhar.isdigit() or len(aadhar) != 12:
            raise ValidationError("Aadhar number must be exactly 12 digits.")
        if Users.objects.exclude(pk=self.instance.pk).filter(aadhar_number=aadhar).exists():
            raise ValidationError("Users with this Aadhar number already exists.")
        return aadhar

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
        valid_skills = [skill[0] for skill in Users.get_primary_skills_choices()]
        if primary_skills not in valid_skills:
            raise ValidationError("Please select a valid primary skill.")
        return primary_skills
    
    def clean(self):
        cleaned_data = super().clean()

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
                user = Users.objects.get(
                    registration_id=registration_id,
                    dob=dob,
                    is_active=True,
                    deleted=False
                )
                cleaned_data['user'] = user
            except Users.DoesNotExist:
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