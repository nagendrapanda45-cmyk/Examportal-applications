import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.users.models import Question

# We need:
# GT: 10 easy, 10 medium, 10 hard (I already did this using update)
# TT Coding: 2 easy, 1 medium, 1 hard
# TT MCQ: 2 easy, 2 medium, 2 hard

def create_tt_questions():
    # TT Coding Easy
    for i in range(5):
        Question.objects.create(
            question_text=f'Coding Easy {i}', correct_answer='A', technical_question_answer='def',
            difficulty='easy', test_type='TT', category_type='Coding', specialisation_name='Python', is_multichoice=False, is_active=True
        )
    # TT Coding Medium
    for i in range(5):
        Question.objects.create(
            question_text=f'Coding Medium {i}', correct_answer='A', technical_question_answer='def',
            difficulty='medium', test_type='TT', category_type='Coding', specialisation_name='Python', is_multichoice=False, is_active=True
        )
    # TT Coding Hard
    for i in range(5):
        Question.objects.create(
            question_text=f'Coding Hard {i}', correct_answer='A', technical_question_answer='def',
            difficulty='hard', test_type='TT', category_type='Coding', specialisation_name='Python', is_multichoice=False, is_active=True
        )
        
    # TT MCQ Easy
    for i in range(5):
        Question.objects.create(
            question_text=f'MCQ Easy {i}', option_a='A', option_b='B', option_c='C', option_d='D', correct_answer='A',
            difficulty='easy', test_type='TT', category_type='MCQs', specialisation_name='Python', is_multichoice=True, is_active=True
        )
    # TT MCQ Medium
    for i in range(5):
        Question.objects.create(
            question_text=f'MCQ Medium {i}', option_a='A', option_b='B', option_c='C', option_d='D', correct_answer='A',
            difficulty='medium', test_type='TT', category_type='MCQs', specialisation_name='Python', is_multichoice=True, is_active=True
        )
    # TT MCQ Hard
    for i in range(5):
        Question.objects.create(
            question_text=f'MCQ Hard {i}', option_a='A', option_b='B', option_c='C', option_d='D', correct_answer='A',
            difficulty='hard', test_type='TT', category_type='MCQs', specialisation_name='Python', is_multichoice=True, is_active=True
        )

create_tt_questions()
print('TT Questions injected successfully!')
