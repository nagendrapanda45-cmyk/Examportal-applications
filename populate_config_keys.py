import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from config_keys.models import ConfigKeys

keys = [
    'date_of_exam',
    'time_of_exam',
    'login_window_duration',
    'gt_duration_minutes',
    'gt_total_questions',
    'gt_easy_questions',
    'gt_medium_questions',
    'gt_hard_questions',
    'tt_duration_minutes',
    'tt_coding_easy_questions',
    'tt_coding_medium_questions',
    'tt_coding_hard_questions',
    'tt_mcq_easy_questions',
    'tt_mcq_medium_questions',
    'tt_mcq_hard_questions',
    'freeze_Small_popup_timesec',
    'freeze_Major_popup_timesec',
    'contact_number',
    'email_sender',
    'email_password',
    'venue_address',
    'programming_languages'
]

for key in keys:
    # keys is the actual name, values is the display name
    ConfigKeys.objects.get_or_create(keys=key, values=key, identifier=key, defaults={'deleted': False, 'year': 2025})

print('Config keys populated successfully!')
