from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.functional import lazy
import os
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
import json
import hashlib
import time
from django.db.models import JSONField
current_year = datetime.now().year

def validate_image(file):
    try:
        max_size_kb = int(Configuration.objects.get(key='photo_max_size_kb').value)
    except (Configuration.DoesNotExist, ValueError):
        max_size_kb = 1024  # Default fallback value
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"Image file too large ( > {max_size_kb}KB )")
    if ext not in valid_extensions:
        raise ValidationError("Unsupported file extension. Only .jpg, .jpeg, .png allowed.")

def validate_resume(file):
    try:
        max_size_mb = int(Configuration.objects.get(key='resume_max_size_mb').value)
    except (Configuration.DoesNotExist, ValueError):
        max_size_mb = 6  # Default fallback value
    ext = os.path.splitext(file.name)[1].lower().strip()
    valid_extensions = ['.pdf', '.doc', '.docx']
    if ext not in valid_extensions:
        raise ValidationError("Only PDF and Word documents (.doc, .docx) are allowed.")
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Resume file size should not exceed {max_size_mb}MB.")

def validate_id_proof(file):
    try:
        max_size_kb = int(Configuration.objects.get(key='id_proof_max_size_kb').value)
    except (Configuration.DoesNotExist, ValueError):
        max_size_kb = 1024  # Default fallback value
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError("Only PDF, JPG, JPEG, or PNG files are allowed.")
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"ID proof file size should not exceed {max_size_kb}KB.")

def validate_certificate(file):
    try:
        max_size_mb = int(Configuration.objects.get(key='certificate_max_size_mb').value)
    except (Configuration.DoesNotExist, ValueError):
        max_size_mb = 6  # Default fallback value
    ext = os.path.splitext(file.name)[1].lower().strip()
    valid_extensions = ['.pdf', '.doc', '.docx']
    if ext not in valid_extensions:
        raise ValidationError("Only PDF and Word documents (.doc, .docx) are allowed.")
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Certificate file size should not exceed {max_size_mb}MB.")



class Users(models.Model):
    def get_upload_path(instance, filename, field_name):
        if not instance.registration_id:
            if not instance.dob:
                raise ValueError("Cannot generate registration_id without dob")
            if not instance.user_id:
                instance._generate_user_id_and_registration_id()
            else:
                dob_str = instance.dob.strftime('%Y%m%d')
                instance.registration_id = f"REG-{timezone.now().year}-{dob_str}-{instance.user_id}"
        return f'{instance.registration_id}/{field_name}_{filename}'

    def photo_upload_path(instance, filename):
        return instance.get_upload_path(filename, 'photo')

    def resume_upload_path(instance, filename):
        return instance.get_upload_path(filename, 'resume')

    def id_proof_upload_path(instance, filename):
        return instance.get_upload_path(filename, 'id_proof')

    def certificate_upload_path(instance, filename):
        return instance.get_upload_path(filename, 'certificate')
    def camera_photo_upload_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'{instance.registration_id}/exam_photo.{ext}'
    def gt_images_upload_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'{instance.registration_id}/gt_images/{int(time.time())}.{ext}'

    def tt_images_upload_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'{instance.registration_id}/tt_images/{int(time.time())}.{ext}'
    def get_primary_skills_choices():
        try:
            from django.db import transaction
            with transaction.atomic():
                current_year = timezone.now().year
                skills = Configuration.objects.filter(
                    key=f'primary_skills_{current_year}',
                    deleted=False
                ).values_list('value', flat=True)
                dynamic_choices = [(skill, skill) for skill in sorted(set(skills))]
        except Exception:
            dynamic_choices = []
        fallback_choices = [
            ('.Net', '.Net'),
            ('PHP', 'PHP'),
            ('Python', 'Python'),
            ('Frontend Developer (Javascript/Angular/React)', 'Frontend Developer (Javascript/Angular/React)'),
            ('QA (Manual/Automation)', 'QA (Manual/Automation)'),
            ('DevOps/Cloud Engineering', 'DevOps/Cloud Engineering'),
            ('Mobile Developer (Android/IOS)', 'Mobile Developer (Android/IOS)'),
            ('Cyber Security', 'Cyber Security'),
            ('Others', 'Others'),
        ]
        return dynamic_choices if dynamic_choices else fallback_choices

    lazy_primary_skills_choices = lazy(get_primary_skills_choices, list)

    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    QUALIFICATION_CHOICES = [
        ('', 'Select your Highest Qualification'),
        ('SSC', 'SSC'), ('Intermediate', 'Intermediate'), ('Diploma', 'Diploma'),
        ('UG', 'UG'), ('PG', 'PG'), ('PhD', 'PhD'), ('Other', 'Other')
    ]
    REFERENCE_CHOICES = [
        ('', 'Select the Reference'),
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    CONFIRMATION_STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Confirmed'),
    ]

    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )

    name_validator = RegexValidator(
        regex=r'^[a-zA-Z\s]+$',
        message="Name should contain only alphabets and spaces."
    )

    aadhar_validator = RegexValidator(
        regex=r'^\d{12}$',
        message="Aadhar number must be exactly 12 digits."
    )

    photo = models.ImageField(
        upload_to=photo_upload_path,
        blank=False,
        null=False,
        validators=[validate_image]
    )

    resume = models.FileField(
        upload_to=resume_upload_path,
        validators=[validate_resume],
        null=False,
        blank=False
    )

    id_proof = models.FileField(
        upload_to=id_proof_upload_path,
        validators=[validate_id_proof],
        null=True,
        blank=True
    )

    certificate = models.FileField(
        upload_to=certificate_upload_path,
        validators=[validate_certificate],
        null=True,
        blank=True
    )
    camera_photo = models.ImageField(
        upload_to=camera_photo_upload_path,
        null=True,
        blank=True
    )
    user_id = models.AutoField(primary_key=True)
    registration_id = models.CharField(max_length=50, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField(null=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    alternative_mobile = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(max_length=2500)
    city = models.CharField(max_length=100)
    pincode = models.CharField(
        max_length=6,
        validators=[RegexValidator(regex=r'^\d{6}$', message='Pincode must contain only 6 digits')]
    )
    primary_skills = models.CharField(
        max_length=100,
        choices=lazy_primary_skills_choices(),
    )
    other_skills = models.TextField(max_length=2500, blank=True, null=True)
    highest_qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES)
    specific_qualification = models.CharField(max_length=255)
    stream = models.CharField(max_length=255, blank=True)
    college_or_university = models.TextField(max_length=2500)
    highest_qualification_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        null=True,
        blank=True
    )
    training_certification = models.TextField(blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, validators=[
        RegexValidator(regex=r'^\d{12}$', message='Enter a valid 12-digit Aadhar number')
    ])

    password = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=5, choices=REFERENCE_CHOICES, default='')
    referred_by = models.CharField(max_length=255, blank=True)
    registered_at = models.DateTimeField(default=timezone.now)
    uploaded_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    registration_mail_sent = models.BooleanField(default=False)
    is_mail_sent = models.BooleanField(default=False)
    action_status = models.CharField(max_length=100, blank=True, null=True, default='pending')
    user_confirmation_status = models.IntegerField(
        choices=CONFIRMATION_STATUS_CHOICES,
        default=0,
        help_text="0: Pending, 1: Confirmed"
    )
    confirmation_token = models.CharField(
        max_length=36,
        unique=True,
        null=True,
        blank=True,
        help_text="UUID token for registration confirmation"
    )
    confirmation_url = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Unique confirmation URL for user registration"
    )
    sh_mail_status = models.BooleanField(default=False, help_text="0: Email not sent, 1: Email sent")
    Notify_mail_status = models.BooleanField(default=False, help_text="0: Email not sent, 1: Email sent")
    invite_mail_status = models.BooleanField(default=False, help_text="0: Email not sent, 1: Email sent")
    invite_email_exception = models.TextField(
        null=True,
        blank=True,
        help_text="Stores exception message if email sending fails"
    )
    is_email_valid = models.BooleanField(default=True)
    latitude = models.FloatField(blank=True, null=True)  # New field for latitude
    longitude = models.FloatField(blank=True, null=True)  # New field for longitude
    ip_address = models.CharField(max_length=45, blank=True, null=True)  # New field for IP address
    active_session_key = models.CharField(max_length=40, null=True, blank=True) # New field for active session key
    submission_mail_sent = models.BooleanField(default=False)
    gt_images = models.JSONField(default=list)
    tt_images= models.JSONField(default=list)
    
    # resolution_mismatch_count = models.IntegerField(default=0)

    def _generate_user_id_and_registration_id(self):
        self._disable_file_fields()
        super().save()
        if self.dob:
            dob_str = self.dob.strftime('%Y%m%d')
            self.registration_id = f"REG-{timezone.now().year}-{dob_str}-{self.user_id}"
        self._enable_file_fields()

    def _disable_file_fields(self):
        self._original_photo = self.photo
        self._original_resume = self.resume
        self._original_id_proof = self.id_proof
        self._original_certificate = self.certificate
        self.photo = None
        self.resume = None
        self.id_proof = None
        self.certificate = None

    def _enable_file_fields(self):
        self.photo = self._original_photo
        self.resume = self._original_resume
        self.id_proof = self._original_id_proof
        self.certificate = self._original_certificate

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def save(self, *args, **kwargs):
        if not self.user_id or not self.registration_id:
            self._generate_user_id_and_registration_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'users'

class ManualResults(models.Model):
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    PASS_FAIL_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('N/A', 'N/A')
    ]

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='manual_results',
        to_field='user_id'
    )
    registration_id = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='manual_results_registration',
        to_field='registration_id'
    )
    general_test_attendance = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    general_test_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    general_test_result = models.CharField(max_length=4, choices=PASS_FAIL_CHOICES)
    technical_test_name = models.CharField(max_length=255, blank=True, null=True)
    technical_test_attendance = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    technical_test_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,
        blank=True
    )
    technical_test_result = models.CharField(max_length=4, choices=PASS_FAIL_CHOICES)

    class Meta:
        db_table = 'manual_results'

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, blank=True, null=True)
    sub_role = models.CharField(max_length=20, choices=[
        ('ProjectManager', 'ProjectManager'), ('TechLead', 'TechLead'), ('HR', 'HR'),
        ('Recruiter', 'Recruiter'), ('SuperAdmin', 'SuperAdmin'), ('Coordinator', 'Coordinator')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'admins'

class Instruction(models.Model):
    TEST_TYPE_CHOICES = [
        ('GT', 'General Test'),
        ('TT', 'Technical Test'),
    ]

    instruction_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=100)
    test_type = models.CharField(max_length=2, choices=TEST_TYPE_CHOICES)
    title = models.CharField(max_length=150)
    content = models.TextField()
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'instructions'
        ordering = ['display_order', 'created_at']

    def __str__(self):
        return self.title
    
class Configuration(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    configID = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        db_table = 'configuration'

class Question(models.Model):
    # @staticmethod
    # @classmethod
    def get_specialisation_choices():
        try:
            from django.db import transaction
            with transaction.atomic():
                languages = Configuration.objects.filter(
                    key='programming_languages_' + str(current_year),
                    deleted=False
                ).values_list('value', flat=True)
                dynamic_choices = [(lang.capitalize(), lang.capitalize()) for lang in sorted(set(languages))]
        except Exception:
            dynamic_choices = []
        fallback_choices = [
            ('Python', 'Python'),
            ('Java', 'Java'),
            ('C', 'C'),
            ('C++', 'C++'),
            ('.NET', '.NET'),
            ('Not Applicable', 'Not Applicable')
        ]
        return dynamic_choices if dynamic_choices else fallback_choices

    lazy_specialisation_choices = lazy(get_specialisation_choices, list)

    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    technical_question_answer = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')],
        blank=True,
        null=True
    )
    difficulty = models.CharField(
        max_length=10,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        blank=True,
        null=True
    )
    test_type = models.CharField(
        max_length=2,
        choices=[('GT', 'General Test'), ('TT', 'Technical Test')]
    )
    category_type = models.CharField(max_length=255, blank=True, null=True)
    specialisation_name = models.CharField(
        max_length=100,
        choices=lazy_specialisation_choices(),
        default='Not Applicable'
    )
    is_multichoice = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text[:50]

    class Meta:
        db_table = 'questions'

class Tests(models.Model):
    TEST_TYPE_CHOICES = [('GT', 'General Test'), ('TT', 'Technical Test')]
    test_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    test_type = models.CharField(max_length=2, choices=TEST_TYPE_CHOICES)
    duration_minutes = models.IntegerField()
    max_duration = models.IntegerField(blank=True, null=True)
    submission_time = models.DateTimeField(blank=True, null=True)
    is_submitted = models.BooleanField(default=False)
    cutoff_pass_score = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    suspicious_activity_count = models.IntegerField(default=0) # New column for suspicious activity count
    test_status = models.IntegerField(default=0)  # New field for test status
    resolution_mismatch_count = models.IntegerField(default=0)
    browser_used = models.CharField(max_length=100, blank=True, null=True)  # New column for browser used


    def __str__(self):
        return f"{self.test_name} - {self.user.full_name}"

    class Meta:
        db_table = 'tests'

class TestUserQuestionAnswer(models.Model):
    attempt_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    user_answer = models.TextField(max_length=1000, blank=True, null=True)
    actual_answer = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(blank=True, null=True)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[
        ('not_answered', 'not_answered'), ('answered', 'answered'), ('review', 'review')
    ], default='not_answered')
    option_order = models.CharField(max_length=10, blank=True, null=True)  # e.g., "B,A,D,C"

    def get_shuffled_options(self):
        if self.option_order:
            order = self.option_order.split(',')
            options = {
                'A': self.question.option_a,
                'B': self.question.option_b,
                'C': self.question.option_c,
                'D': self.question.option_d
            }
            return [(opt, options[opt]) for opt in order if options[opt]]
        return [
            ('A', self.question.option_a),
            ('B', self.question.option_b),
            ('C', self.question.option_c),
            ('D', self.question.option_d)
        ]

    def __str__(self):
        return f"Answer for {self.question} by {self.user.full_name}"

    class Meta:
        db_table = 'test_user_questions_answers'

class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    total_attempted_questions = models.IntegerField()
    total_correct_answers = models.IntegerField()
    percentage = models.FloatField()
    cutoff_pass_score = models.IntegerField(blank=True, null=True)
    result_status = models.CharField(max_length=10, choices=[('pass', 'pass'), ('fail', 'fail')])
    generated_at = models.DateTimeField(auto_now_add=True)
    skill = models.CharField(max_length=100, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.total_questions > 0:
            self.percentage = (self.total_correct_answers / self.total_questions) * 100
        else:
            self.percentage = 0.0
        if self.cutoff_pass_score is not None:
            self.result_status = 'pass' if self.total_correct_answers >= self.cutoff_pass_score else 'fail'
        super().save(*args, **kwargs)
        final_result, created = FinalResult.objects.get_or_create(user=self.user)
        if not created:
            final_result.result_status = final_result.calculate_result_status()
            final_result.save()
    def __str__(self):
        return f"Result for {self.user.full_name} - {self.result_status}"
    class Meta:
        db_table = 'results'
class GenerateTest(models.Model):
    TEST_TYPE_CHOICES = [('GT', 'General Test'), ('TT', 'Technical Test')]
    set_name = models.CharField(max_length=50, unique=True)
    pdf_file = models.FileField(upload_to='test_pdfs/')
    test_type = models.CharField(max_length=2, choices=TEST_TYPE_CHOICES, default='GT')
    created_at = models.DateTimeField(auto_now_add=True)
    batch_id = models.CharField(max_length=50, null=True)
    class Meta:
        db_table = 'generate_test'
    def __str__(self):
        return f"{self.set_name} ({self.get_test_type_display()})"
class GenerateTestQuestions(models.Model):
    generate_test = models.ForeignKey(GenerateTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    class Meta:
        db_table = 'generate_test_questions'
    def __str__(self):
        return f"{self.generate_test.set_name} - {self.question.question_text[:50]}..."
class FinalResult(models.Model):
    final_result_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    result_status = models.CharField(max_length=10, choices=[('pass', 'pass'), ('fail', 'fail')])
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_result_published = models.BooleanField(default=False)
    def calculate_result_status(self):
        gt_result = Result.objects.filter(user=self.user, test__test_type='GT').order_by('-generated_at').first()
        tt_result = Result.objects.filter(user=self.user, test__test_type='TT').order_by('-generated_at').first()
        if gt_result and tt_result:
            gt_status = gt_result.result_status
            tt_status = tt_result.result_status
            return 'pass' if (gt_status == 'pass' and tt_status == 'pass') else 'fail'
        elif gt_result:
            return gt_result.result_status
        elif tt_result:
            return tt_result.result_status
        else:
            return 'fail'
    def save(self, *args, **kwargs):
        if not self.pk:
            self.result_status = self.calculate_result_status()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Final Result for {self.user.full_name} - {self.result_status}"
    class Meta:
        db_table = 'final_results'
