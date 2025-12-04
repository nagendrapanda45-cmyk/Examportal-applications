from django import forms
import logging
from home.users.models import Tests, Instruction, Users
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from config_keys.models import ConfigKeys 
from django import forms
from home.users.models import Configuration, FinalResult
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator
import re
from django.core.exceptions import ValidationError

current_year = datetime.now().year

logger = logging.getLogger(__name__)

User = get_user_model()

class TestForm(forms.ModelForm):
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    user = forms.ModelChoiceField(
        queryset=Users.objects.filter(is_active=True, deleted=False),
        required=True,
        to_field_name='registration_id',
        label='User Registration ID'
    )

    class Meta:
        model = Tests
        fields = [
            'user', 'test_name', 'description', 'test_type',
            'duration_minutes', 'max_duration',
            'start_time', 'cutoff_pass_score'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        now = timezone.now().strftime('%Y-%m-%dT%H:%M')
        self.fields['start_time'].widget.attrs['min'] = now
        if self.request and not self.request.user.is_staff:
            self.fields['user'].queryset = Users.objects.filter(id=self.request.user.id, is_active=True, deleted=False, is_superuser=False)
            self.fields['user'].initial = self.request.user
            self.fields['user'].widget.attrs['readonly'] = True
        # Customize dropdown display
        self.fields['user'].label_from_instance = lambda obj: obj.registration_id

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        duration = cleaned_data.get('max_duration')
        duration_minutes = cleaned_data.get('duration_minutes')
        if start and start < timezone.now():
            raise forms.ValidationError("Start time cannot be in the past")
        if duration and duration <= 0:
            raise forms.ValidationError("Max duration must be positive")
        if duration_minutes and duration_minutes <= 0:
            raise forms.ValidationError("Duration minutes must be positive")
        return cleaned_data

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['test_name', 'test_type', 'title', 'content', 'display_order', 'is_active']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'test_type': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(),
        }
class ConfigurationForm(forms.ModelForm):
    key = forms.CharField(
        label='Configuration Key',
        required=False,  # Handled dynamically in __init__
    )

    class Meta:
        model = Configuration
        fields = ['value', 'deleted']
        widgets = {
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter configuration value'
            }),
            'deleted': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch'
            }),
        }
        labels = {
            'value': 'Configuration Value',
            'deleted': 'Mark as Inactive'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = datetime.now().year  # 2025

        if self.instance and self.instance.pk:
            display_key = self.instance.key
            try:
                config_key = ConfigKeys.objects.get(id=self.instance.configID)
                display_key = config_key.values
            except ConfigKeys.DoesNotExist:
                logger.warning(f"ConfigKeys entry not found for configID={self.instance.configID}")
            
            self.fields['key'] = forms.CharField(
                initial=display_key,
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                label='Configuration Key',
                required=False
            )
        else:
            config_keys = ConfigKeys.objects.filter(deleted=False)
            choices = [('', 'Select Configuration')] + [(str(ck.id), ck.values) for ck in config_keys]
            self.fields['key'] = forms.ChoiceField(
                choices=choices,
                widget=forms.Select(attrs={'class': 'form-control'}),
                label='Configuration Key',
                required=True
            )

            self.fields['key'].initial = ''
            logger.debug(f"New instance, key choices: {choices}")

            self.fields['value'] = forms.CharField(
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter configuration value'}),
                label='Configuration Value',
                required=True
            )

    def clean(self):
        cleaned_data = super().clean()
        value = cleaned_data.get('value')
        deleted = cleaned_data.get('deleted')
        current_year = datetime.now().year  # 2025
        current_date = timezone.now().date()  # 2025-07-22

        if self.instance and self.instance.pk:
            key_id = self.instance.configID
            key = self.instance.key
        else:
            key_id = cleaned_data.get('key')
            if not key_id:
                self.add_error('key', 'Please select a configuration key.')
                return cleaned_data
            try:
                config_key = ConfigKeys.objects.get(id=key_id)
                key = config_key.keys
            except ConfigKeys.DoesNotExist:
                self.add_error('key', 'Selected key does not exist.')
                return cleaned_data

        if not value:
            self.add_error('value', 'Configuration value cannot be empty.')
        if key.startswith('gt_') and 'questions' in key:
            try:
                current_value = int(value)
                if current_value < 0:
                    self.add_error('value', 'Number of questions cannot be negative.')
            except ValueError:
                self.add_error('value', 'Number of questions must be a valid integer.')
            if key != f'gt_total_questions_{current_year}':
                gt_configs = Configuration.objects.filter(
                    key__in=[
                        f'gt_total_questions_{current_year}',
                        f'gt_easy_questions_{current_year}',
                        f'gt_medium_questions_{current_year}',
                        f'gt_hard_questions_{current_year}'
                    ],
                    deleted=False
                ).values('key', 'value')
                gt_values = {config['key']: int(config['value']) for config in gt_configs if config['value'].isdigit()}
                total = gt_values.get(f'gt_total_questions_{current_year}', 0)
                easy = gt_values.get(f'gt_easy_questions_{current_year}', 0)
                medium = gt_values.get(f'gt_medium_questions_{current_year}', 0)
                hard = gt_values.get(f'gt_hard_questions_{current_year}', 0)

                if total == 0 and key != f'gt_total_questions_{current_year}':
                    self.add_error('value', f"Total questions (gt_total_questions_{current_year}) must be set first.")
                    return cleaned_data

                if key == f'gt_easy_questions_{current_year}':
                    easy = current_value
                elif key == f'gt_medium_questions_{current_year}':
                    medium = current_value
                elif key == f'gt_hard_questions_{current_year}':
                    hard = current_value

                running_sum = easy + medium + hard
                if running_sum > total:
                    self.add_error(
                        'value',
                        f'The sum of easy ({easy}), medium ({medium}), and hard ({hard}) questions ({running_sum}) '
                        f'exceeds the total questions ({total}) for General Test.'
                    )

                existing_counts = [
                    gt_values.get(f'gt_easy_questions_{current_year}', 0),
                    gt_values.get(f'gt_medium_questions_{current_year}', 0),
                    gt_values.get(f'gt_hard_questions_{current_year}', 0)
                ]
                set_count_before = sum(1 for x in existing_counts if x > 0)
                set_count = sum(1 for x in [easy, medium, hard] if x > 0)

                if set_count_before == 2 or (set_count == 3 and set_count_before < 2):
                    remaining = total - (running_sum - current_value)
                    if current_value != remaining:
                        self.add_error(
                            'value',
                            f'The sum of easy ({easy}), medium ({medium}), and hard ({hard}) questions ({running_sum}) '
                            f'must equal the total questions ({total}) for General Test. Value must be {remaining}.'
                        )

        # Validation for Technical Test question counts
        if key.startswith('tt_') and 'questions' in key:
            try:
                current_value = int(value)
                if current_value < 0:
                    self.add_error('value', 'Number of questions cannot be negative.')
            except ValueError:
                self.add_error('value', 'Number of questions must be a valid integer.')
            if key != f'tt_total_questions_{current_year}':
                tt_configs = Configuration.objects.filter(
                    key__in=[
                        f'tt_total_questions_{current_year}',
                        f'tt_coding_easy_questions_{current_year}',
                        f'tt_coding_medium_questions_{current_year}',
                        f'tt_coding_hard_questions_{current_year}',
                        f'tt_mcq_easy_questions_{current_year}',
                        f'tt_mcq_medium_questions_{current_year}',
                        f'tt_mcq_hard_questions_{current_year}'
                    ],
                    deleted=False
                ).values('key', 'value')
                tt_values = {config['key']: int(config['value']) for config in tt_configs if config['value'].isdigit()}
                total = tt_values.get(f'tt_total_questions_{current_year}', 0)
                coding_easy = tt_values.get(f'tt_coding_easy_questions_{current_year}', 0)
                coding_medium = tt_values.get(f'tt_coding_medium_questions_{current_year}', 0)
                coding_hard = tt_values.get(f'tt_coding_hard_questions_{current_year}', 0)
                mcq_easy = tt_values.get(f'tt_mcq_easy_questions_{current_year}', 0)
                mcq_medium = tt_values.get(f'tt_mcq_medium_questions_{current_year}', 0)
                mcq_hard = tt_values.get(f'tt_mcq_hard_questions_{current_year}', 0)

                if total == 0 and key != f'tt_total_questions_{current_year}':
                    self.add_error('value', f"Total questions (tt_total_questions_{current_year}) must be set first.")
                    return cleaned_data

                if key == f'tt_coding_easy_questions_{current_year}':
                    coding_easy = current_value
                elif key == f'tt_coding_medium_questions_{current_year}':
                    coding_medium = current_value
                elif key == f'tt_coding_hard_questions_{current_year}':
                    coding_hard = current_value
                elif key == f'tt_mcq_easy_questions_{current_year}':
                    mcq_easy = current_value
                elif key == f'tt_mcq_medium_questions_{current_year}':
                    mcq_medium = current_value
                elif key == f'tt_mcq_hard_questions_{current_year}':
                    mcq_hard = current_value

                running_sum = coding_easy + coding_medium + coding_hard + mcq_easy + mcq_medium + mcq_hard
                if running_sum > total:
                    self.add_error(
                        'value',
                        f'The sum of coding and MCQ questions ({running_sum}) exceeds the total questions ({total}) for Technical Test.'
                    )

                existing_counts = [
                    tt_values.get(f'tt_coding_easy_questions_{current_year}', 0),
                    tt_values.get(f'tt_coding_medium_questions_{current_year}', 0),
                    tt_values.get(f'tt_coding_hard_questions_{current_year}', 0),
                    tt_values.get(f'tt_mcq_easy_questions_{current_year}', 0),
                    tt_values.get(f'tt_mcq_medium_questions_{current_year}', 0),
                    tt_values.get(f'tt_mcq_hard_questions_{current_year}', 0)
                ]
                set_count_before = sum(1 for x in existing_counts if x > 0)
                set_count = sum(1 for x in [coding_easy, coding_medium, coding_hard, mcq_easy, mcq_medium, mcq_hard] if x > 0)

                if set_count_before >= 5 or (set_count == 6 and set_count_before < 5):
                    remaining = total - (running_sum - current_value)
                    if current_value != remaining:
                        self.add_error(
                            'value',
                            f'The sum of coding and MCQ questions ({running_sum}) must equal the total questions ({total}) for Technical Test. Value must be {remaining}.'
                        )

        # Validation for General Test cutoff score
        if key == f'gt_cutoff_pass_score_{current_year}':
            gt_total_config = Configuration.objects.filter(
                key=f'gt_total_questions_{current_year}',
                deleted=False
            ).values('value').first()
            if not gt_total_config or not gt_total_config['value'].isdigit():
                self.add_error('value', f"Total questions (gt_total_questions_{current_year}) must be set first.")
                return cleaned_data
            total_questions = int(gt_total_config['value'])
            try:
                cutoff = int(value)
                if cutoff < 0:
                    self.add_error('value', 'Cutoff score cannot be negative.')
            except ValueError:
                self.add_error('value', 'Cutoff score must be a valid integer.')
            if cutoff > total_questions:
                self.add_error('value', f"Cutoff score ({cutoff}) cannot exceed total questions ({total_questions}).")

        # Validation for Technical Test cutoff score
        if key == f'tt_cutoff_pass_score_{current_year}':
            tt_total_config = Configuration.objects.filter(
                key=f'tt_total_questions_{current_year}',
                deleted=False
            ).values('value').first()
            if not tt_total_config or not tt_total_config['value'].isdigit():
                self.add_error('value', f"Total questions (tt_total_questions_{current_year}) must be set first.")
                return cleaned_data
            total_questions = int(tt_total_config['value'])
            try:
                cutoff = int(value)
                if cutoff < 0:
                    self.add_error('value', 'Cutoff score cannot be negative.')
            except ValueError:
                self.add_error('value', 'Cutoff score must be a valid integer.')
            if cutoff > total_questions:
                self.add_error('value', f"Cutoff score ({cutoff}) cannot exceed total questions ({total_questions}).")

        # Validation for contact_numbers_2025
        if key == f'contact_numbers_{current_year}':
            if not re.match(r'^\d{10}(?: / \d{10})*$', value):
                self.add_error('value', 'Contact numbers must be one or two 10-digit numbers separated by " / " (e.g., "7842181883 / 9063839747").')

        # Validation for date_of_exam_2025
        if key == f'date_of_exam_{current_year}':
            try:
                exam_date = datetime.strptime(value, '%Y-%m-%d').date()
                if exam_date <= current_date:
                    self.add_error('value', 'Date of exam must be a future date.')
            except ValueError:
                self.add_error('value', 'Date of exam must be in YYYY-MM-DD format.')

        # Validation for time_of_exam_2025 and slot_timings_2025
        time_keys = [f'time_of_exam_{current_year}', f'slot_timings_{current_year}']
        if key in time_keys:
            if not re.match(r'^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM|am|pm)$|^Slot \d+: (0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM|am|pm) - (0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM|am|pm)$', value):
                self.add_error('value', 'Time must be in HH:MM AM/PM format (e.g., "10:00 AM") or slot format (e.g., "Slot 1: 09:00 AM - 11:00 AM").')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not (self.instance and self.instance.pk):
            key_id = self.cleaned_data['key']
            config_key = ConfigKeys.objects.get(id=key_id)
            instance.key = config_key.keys
            instance.configID = str(config_key.id)

        keys_allowing_multiple_active = [
            f'primary_skills_{current_year}',
            f'email_template_{current_year}',
            f'programming_languages_{current_year}',
        ]

        if not instance.deleted and instance.key not in keys_allowing_multiple_active:
            other_configs = Configuration.objects.filter(key=instance.key)
            if instance.pk:
                other_configs = other_configs.exclude(pk=instance.pk)
            if other_configs.exists():
                other_configs.update(deleted=True)

        if commit:
            instance.save()
        return instance

class GenerateTestForm(forms.Form):
    num_sets = forms.IntegerField(
        label='Number of Test Sets',
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
        required=True
    )
    
    generate_by_difficulty = forms.ChoiceField(
        choices=[('yes', 'Yes (Proceed by configurations)'), ('no', 'No (Set Manually)')],
        widget=forms.Select(attrs={'class': 'form-control form-control-lg', 'id': 'generateByDifficulty'}),
        initial='yes',
        required=True
    )

    programming_language = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        label='Programming Language',
        required=False
    )

    # These hidden fields are populated by JavaScript in the template for manual mode
    num_easy = forms.IntegerField(required=False, widget=forms.HiddenInput())
    num_medium = forms.IntegerField(required=False, widget=forms.HiddenInput())
    num_hard = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        # Pop custom arguments before calling super
        self.test_type = kwargs.pop('test_type', 'gt')
        self.configured_total = kwargs.pop('configured_total', 0)
        programming_languages = kwargs.pop('programming_languages', [])  # Get from view context
        super().__init__(*args, **kwargs)

        # Dynamically populate programming language choices only for Technical Tests
        if self.test_type == 'tt':
            if programming_languages:
                self.fields['programming_language'].choices = [('', 'Select a language')] + sorted([(lang, lang) for lang in programming_languages])
            else:
                # Fallback to querying primary_skills_{current_year} if not provided
                current_year = datetime.now().year
                try:
                    languages = set(Configuration.objects.filter(key=f'primary_skills_{current_year}', deleted=False).values_list('value', flat=True))
                    self.fields['programming_language'].choices = [('', 'Select a language')] + sorted([(lang, lang) for lang in languages])
                except Exception:
                    self.fields['programming_language'].choices = [('', 'Select a language')]
        else:
            # Hide the programming language field if not a technical test
            self.fields['programming_language'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        mode = cleaned_data.get('generate_by_difficulty')
        
        # Validate that a programming language is selected for Technical Tests
        if self.test_type == 'tt' and not cleaned_data.get('programming_language'):
            self.add_error('programming_language', 'This field is required for Technical Tests.')
            
        # Perform server-side validation only for manual difficulty mode ('no')
        if mode == 'no':
            num_easy = cleaned_data.get('num_easy')
            num_medium = cleaned_data.get('num_medium')
            num_hard = cleaned_data.get('num_hard')

            # Check if values were provided from the hidden fields
            if num_easy is None or num_medium is None or num_hard is None:
                raise ValidationError("Easy, Medium, and Hard question counts are required for manual setup. Please enter a number for each.")

            # Validation 1: Check if each value is between 1 and 15
            if not (1 <= num_easy <= 15 and 1 <= num_medium <= 15 and 1 <= num_hard <= 15):
                self.add_error(None, "Validation Failed: When setting manually, each difficulty count must be between 1 and 15.")

            # Validation 2: Check if the sum matches the configured total
            manual_total = num_easy + num_medium + num_hard
            if self.configured_total > 0 and manual_total != self.configured_total:
                self.add_error(None, f"Validation Failed: The sum of manual questions ({manual_total}) must equal the configured total of {self.configured_total}.")
            elif self.configured_total <= 0:
                self.add_error(None, "Configuration Error: The total number of questions for this test type is not configured or is zero. Please set it in Configurations.")

        return cleaned_data
class FinalResultForm(forms.ModelForm):
    class Meta:
        model = FinalResult
        fields = ['result_status']
        widgets = {
            'result_status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'result_status': 'Final Result Status',
        }