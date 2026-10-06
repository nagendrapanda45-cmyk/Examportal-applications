import os, django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.users.models import Configuration

current_year = datetime.now().year

configs_to_add = [
    (f'programming_languages_{current_year}', 'Python'),
    (f'programming_languages_{current_year}', 'Java'),
    (f'programming_languages_{current_year}', 'C++'),
    (f'gt_total_questions_{current_year}', '30'),
    (f'gt_easy_questions_{current_year}', '10'),
    (f'gt_medium_questions_{current_year}', '10'),
    (f'gt_hard_questions_{current_year}', '10'),
    (f'tt_total_questions_{current_year}', '10'),
    (f'tt_easy_questions_{current_year}', '4'),
    (f'tt_medium_questions_{current_year}', '3'),
    (f'tt_hard_questions_{current_year}', '3'),
]

for key, val in configs_to_add:
    if not Configuration.objects.filter(key=key, value=val, deleted=False).exists():
        Configuration.objects.create(key=key, value=val, deleted=False)

print('Configurations auto-injected!')
