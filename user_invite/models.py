# from django.db import models
# from home.users.models import Configuration, Users
# from django.utils import timezone

# class UserInvite(models.Model):
#     """
#     Model to track user invitations for the exam portal.
#     """
#     user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
#     invited_status = models.CharField(
#         max_length=20,
#         choices=[('registered', 'Registered'), ('invited', 'Invited')],
#         default='registered',
#         help_text="Status of the user invite"
#     )
#     invitation_date = models.DateTimeField(default=timezone.now, help_text="Date and time of invitation")
#     date_of_exam = models.DateField(null=True, blank=True, help_text="Date of the exam")
#     start_time_slot = models.TimeField(null=True, blank=True, help_text="Start time slot of the exam")
#     end_time_slot = models.TimeField(null=True, blank=True, help_text="End time slot of the exam")
#     is_mail_sent = models.BooleanField(default=False, help_text="Indicates if the email was sent")
#     is_bulk_mail_sent = models.BooleanField(default=False, help_text="Indicates if bulk email was sent")
#     is_deleted = models.BooleanField(default=False, help_text="Soft delete flag")
#     created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the invite was created")
#     email_template_used = models.CharField(max_length=100, null=True, blank=True)

#     class Meta:
#         db_table = 'user_invites'
#         verbose_name = 'User Invite'
#         verbose_name_plural = 'User Invites'

#     def __str__(self):
#         return f"{self.user.full_name} - {self.invited_status}"

#     def save(self, *args, **kwargs):
#         """
#         Override save method to ensure invitation details are updated.
#         """
#         super().save(*args, **kwargs)

# def get_email_template_choices():
#     current_year = '2025'  # Replace with dynamic year if needed, e.g., datetime.now().year
#     try:
#         return [(config.value, config.value) for config in Configuration.objects.filter(key__startswith=f'email_template_{current_year}', deleted=False)]
#     except Exception:
#         return []  # Return empty choices during migration

# class EmailTemplate(models.Model):
#     email_id = models.AutoField(primary_key=True)
#     email_template = models.CharField(max_length=100, choices=get_email_template_choices())  # Call the function
#     email_context = models.TextField()
#     is_deleted = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'email_templates'

#     def __str__(self):
#         return self.email_template
# user_invite/models.py
from django.db import models
from home.users.models import Configuration, Users
from django.utils import timezone

class UserInvite(models.Model):
    """
    Model to track user invitations for the exam portal.
    """
    user = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    invited_status = models.CharField(
        max_length=20,
        choices=[('registered', 'Registered'), ('invited', 'Invited')],
        default='registered',
        help_text="Status of the user invite"
    )
    invitation_date = models.DateTimeField(default=timezone.now, help_text="Date and time of invitation")
    date_of_exam = models.DateField(null=True, blank=True, help_text="Date of the exam")
    start_time_slot = models.TimeField(null=True, blank=True, help_text="Start time slot of the exam")
    end_time_slot = models.TimeField(null=True, blank=True, help_text="End time slot of the exam")
    is_mail_sent = models.BooleanField(default=False, help_text="Indicates if the email was sent")
    is_bulk_mail_sent = models.BooleanField(default=False, help_text="Indicates if bulk email was sent")
    is_deleted = models.BooleanField(default=False, help_text="Soft delete flag")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the invite was created")
    email_template_used = models.CharField(max_length=100, null=True, blank=True)
    pre_assigned_questions = models.JSONField(blank=True, null=True)  # Store {'GT': [ids], 'TT': [ids]}

    def set_pre_assigned_questions(self, question_ids):
        """Set the pre-assigned question IDs and save."""
        self.pre_assigned_questions = question_ids
        self.save(update_fields=['pre_assigned_questions'])

    def get_pre_assigned_questions(self):
        """Get the pre-assigned question IDs or empty dict."""
        return self.pre_assigned_questions or {'GT': [], 'TT': []}
    # Add the new field to track email type
    email_type_sent = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Type of email sent (e.g., call_letter, invitation_letter, reminder_letter)"
    )
    slot_remainder_mail = models.BooleanField(
    default=False,
    help_text="Indicates if reminder mail for slot was sent"
    )

    class Meta:
        db_table = 'user_invites'
        verbose_name = 'User Invite'
        verbose_name_plural = 'User Invites'

    def __str__(self):
        return f"{self.user.full_name} - {self.invited_status}"

    def save(self, *args, **kwargs):
        """
        Override save method to ensure invitation details are updated.
        """
        super().save(*args, **kwargs)

def get_email_template_choices():
    current_year = '2025'  # Replace with dynamic year if needed, e.g., datetime.now().year
    try:
        return [(config.value, config.value) for config in Configuration.objects.filter(key__startswith=f'email_template_{current_year}', deleted=False)]
    except Exception:
        return []  # Return empty choices during migration

class EmailTemplate(models.Model):
    email_id = models.AutoField(primary_key=True)
    email_template = models.CharField(max_length=100, choices=get_email_template_choices())
    subject = models.CharField(max_length=200, blank=False, null=False, default="")

    email_context = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'email_templates'

    def __str__(self):
        return self.email_template