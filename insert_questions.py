import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.users.models import Question

Question.objects.all().delete()

# Create 35 GT questions to be safe
for i in range(1, 36):
    Question.objects.create(
        question_text=f'Sample General Test Question {i}',
        option_a='A', option_b='B', option_c='C', option_d='D',
        correct_answer='A',
        difficulty='easy',
        test_type='GT',
        category_type='Aptitude',
        is_multichoice=False,
        is_active=True
    )

# Create 35 TT questions for Python
for i in range(1, 36):
    Question.objects.create(
        question_text=f'Sample Technical Python Question {i}',
        option_a='A', option_b='B', option_c='C', option_d='D',
        correct_answer='A',
        difficulty='easy',
        test_type='TT',
        category_type='MCQs',
        specialisation_name='Python',
        is_multichoice=False,
        is_active=True
    )

# Also create some coding questions
for i in range(1, 6):
    Question.objects.create(
        question_text=f'Write a Python function for task {i}',
        correct_answer='A', # using A instead of long string to avoid max_length issues
        technical_question_answer='def solution(): return True',
        difficulty='medium',
        test_type='TT',
        category_type='Coding',
        specialisation_name='Python',
        is_multichoice=False,
        is_active=True
    )

print(f"Total questions in DB: {Question.objects.count()}")
