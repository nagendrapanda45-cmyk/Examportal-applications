# ... all your imports ...
import logging
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from home.users.models import Tests, Instruction, Result, Question, TestUserQuestionAnswer, GenerateTest, GenerateTestQuestions
from home.users.models import Users
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import os
import pandas as pd
import random
from collections import defaultdict
from django.http import HttpResponse
from django.core.files import File
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestForm, InstructionForm,GenerateTestForm,FinalResultForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.core.mail import send_mail
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta
import zipfile
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from reportlab.platypus import PageBreak
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from home.users.models import Configuration,FinalResult,ManualResults
from .forms import ConfigurationForm
from django.db.models import Count
from django.urls import reverse
from django.db.models import Count,Avg,Q
from config_keys.models import ConfigKeys
import json


# ... (rest of your views.py file from index to result_view) ...
def index(request):
    return redirect('admin:index')

logger=logging.getLogger(__name__)

current_year = datetime.now().year

@login_required
def test_list(request):
    # Get queryset based on user role
    if request.user.is_staff:
        tests = Tests.objects.select_related('user').all()
    else:
        tests = Tests.objects.select_related('user').filter(user=request.user)
 
    # Search filters
    user_query = request.GET.get('user_query', '').strip()
    test_type = request.GET.get('test_type', '')
 
    if user_query:
        tests = tests.filter(
            Q(user__first_name__icontains=user_query) |
            Q(user__last_name__icontains=user_query)|
            Q(user__registration_id__icontains=user_query)|
            Q(test_name__icontains=user_query)
        )
    if test_type:
        tests = tests.filter(test_type=test_type)
 
    tests = tests.order_by('-test_id')  # Order by test_id descending
 
    # Update test status
    now = timezone.now().replace(microsecond=0)
    updated_count = 0
    for test in tests:
        if test.start_time and test.end_time:
            if now > test.end_time and not test.is_submitted ==0:
                test.is_submitted = 1
                test.submission_time = now
                test.save(update_fields=['is_submitted', 'submission_time'])
                updated_count += 1
                logger.info(f"Test {test.test_name} (ID: {test.pk}) auto-submitted for user {test.user.user_id} at {now}")
 
    if updated_count > 0:
        logger.info(f"test_list view: Auto-submitted {updated_count} test(s) at {now}")
 
    paginator = Paginator(tests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/tests/test_list.html', {
        'page_obj': page_obj,
        'now': now,
    })
 
 
@login_required
def test_view(request, pk):
    test = get_object_or_404(
        Tests.objects.select_related('user').prefetch_related('testuserquestionanswer_set__question'),
        pk=pk
    )
    if not request.user.is_staff and test.user != request.user:
        logger.warning(f"User {request.user.id} attempted unauthorized access to test {test.pk}")
        return render(request, 'home/error.html', {
            'message': "You are not authorized to view this test."
        }, status=403)
 
    question_answers = TestUserQuestionAnswer.objects.filter(
        test=test,
        user=test.user,
        user_answer__isnull=False
    ).exclude(
        user_answer=''
    ).select_related('question').order_by('question__question_id')
 
    if request.method == 'POST' and test.test_type == 'TT' and request.user.is_staff:
        for qa in question_answers:
            if not qa.question.correct_answer:
                is_correct = request.POST.get(f'correct_{qa.attempt_id}') == 'on'
                qa.is_correct = is_correct
                qa.score = 1 if is_correct else 0
                qa.save()
 
        total_attempted_questions = question_answers.count()
        total_questions = TestUserQuestionAnswer.objects.filter(
            test=test,
            user=test.user
        ).count()
        total_correct = question_answers.filter(is_correct=True).count()
        percentage = (total_correct / total_questions) * 100 if total_questions > 0 else 0
 
        results = Result.objects.filter(test=test, user=test.user).order_by('-generated_at')
        cutoff_score = 0
 
        if results.exists():
            existing_result = results.first()
            cutoff_score = existing_result.cutoff_pass_score if existing_result.cutoff_pass_score is not None else 0
            result_status = 'pass' if total_correct >= cutoff_score else 'fail'
 
            Result.objects.filter(pk=existing_result.pk).update(
                total_correct_answers=total_correct,
                percentage=percentage,
                result_status=result_status,
                generated_at=timezone.now()
            )
            result = results.first()
        else:
            result_status = 'pass' if total_correct >= cutoff_score else 'fail'
            result = Result.objects.create(
                test=test,
                user=test.user,
                total_questions=total_questions,
                total_attempted_questions=total_attempted_questions,
                total_correct_answers=total_correct,
                percentage=percentage,
                cutoff_pass_score=cutoff_score,
                result_status=result_status
            )
 
        user = test.user
        gt_result = Result.objects.filter(user=user, test__test_type='GT').order_by('-generated_at').first()
        tt_result = result
 
        if gt_result and tt_result:
            final_status = 'pass' if (
                gt_result.result_status.lower() == 'pass' and
                tt_result.result_status.lower() == 'pass'
            ) else 'fail'
           
            final_result, created = FinalResult.objects.update_or_create(
                user=user,
                defaults={
                    'result_status': final_status,
                    'updated_at': timezone.now()
                }
            )
            if created:
                final_result.generated_at = timezone.now()
                final_result.save()
 
        messages.success(request, "Test results updated successfully!")
        return redirect('test_view', pk=test.pk)
 
    paginator = Paginator(question_answers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    return render(request, 'home/tests/test_view.html', {
        'test': test,
        'user': test.user,
        'question_answers': question_answers,
        'page_obj': page_obj,
        'is_technical_test': test.test_type == 'TT'
    })
 
@login_required
def test_edit(request, pk):
    test = get_object_or_404(Tests.objects.select_related('user'), pk=pk)
    if not request.user.is_staff:
        logger.warning(f"User {request.user.id} attempted unauthorized access to edit test {test.pk}")
        return render(request, 'home/error.html', {
            'message': "You are not authorized to edit this test."
        }, status=403)
 
    if request.method == 'POST':
        try:
            is_submitted_value = request.POST.get('is_submitted')
           
            if is_submitted_value == 'True':
                test.is_submitted = 1
                if not test.submission_time:
                    test.submission_time = timezone.now().replace(microsecond=0)
                update_fields = ['is_submitted', 'submission_time']
            else:
                test.is_submitted = 0
                update_fields = ['is_submitted']
           
            test.save(update_fields=update_fields)
            messages.success(request, f"Test status updated successfully!")
            logger.info(f"User {request.user.id} edited test {test.test_name} (ID: {test.pk}) is_submitted to {test.is_submitted}, submission_time to {test.submission_time}")
            return redirect('test_list')
        except Exception as e:
            logger.error(f"Failed to save test {test.pk}: {str(e)}")
            messages.error(request, "An error occurred while saving the test. Please try again.")
            return render(request, 'home/tests/test_edit.html', {'test': test})
 
    return render(request, 'home/tests/test_edit.html', {
        'test': test,
    })
 
@login_required
def instruction_list(request):
    instructions = Instruction.objects.all().order_by('display_order')
    test_name_query = request.GET.get('test_name_query', '')
    test_type = request.GET.get('test_type', '')

    if test_name_query:
        instructions = instructions.filter(test_name__icontains=test_name_query)
    if test_type:
        instructions = instructions.filter(test_type=test_type)

    test_type_choices = Instruction.TEST_TYPE_CHOICES
    paginator = Paginator(instructions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/instructions/instruction_list.html', {
        'page_obj': page_obj,
        'test_type_choices': test_type_choices,
        'test_name_query': test_name_query,
        'test_type': test_type,
    })
@login_required
def instruction_add(request):
    if request.method == 'POST':
        form = InstructionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instruction added successfully.')
            return redirect('instruction_list')
    else:
        form = InstructionForm()
    return render(request, 'home/instructions/instruction_form.html', {'form': form})
@login_required
def instruction_edit(request, pk):
    instruction = get_object_or_404(Instruction, pk=pk)
    if request.method == 'POST':
        form = InstructionForm(request.POST, instance=instruction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instruction updated successfully.')
            return redirect('instruction_list')
    else:
        form = InstructionForm(instance=instruction)
    return render(request, 'home/instructions/instruction_form.html', {'form': form})
@login_required
def instruction_delete(request, pk):
    instruction = get_object_or_404(Instruction, pk=pk)
    instruction.delete()
    messages.success(request, 'Instruction deleted successfully.')
    return redirect('instruction_list')

@login_required
def result_list(request):
    min_percentage = request.GET.get('min_percentage')
    max_percentage = request.GET.get('max_percentage')
    result_status = request.GET.get('result_status')
    user_query = request.GET.get('user_query')
 
    results = Result.objects.select_related('user', 'test').all()
 
    if user_query:
        results = results.filter(
            Q(user__first_name__icontains=user_query) |
            Q(user__last_name__icontains=user_query) |
            Q(test__test_name__icontains=user_query) |
            Q(user__registration_id__icontains=user_query)
        )
    if min_percentage:
        try:
            results = results.filter(percentage__gte=float(min_percentage))
        except ValueError:
            logger.warning(f"Invalid min_percentage: {min_percentage}")
    if max_percentage:
        try:
            results = results.filter(percentage__lte=float(max_percentage))
        except ValueError:
            logger.warning(f"Invalid max_percentage: {max_percentage}")
    if result_status:
        results = results.filter(result_status=result_status.upper())
 
    paginator = Paginator(results.order_by('-result_id'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    context = {
        'page_obj': page_obj,
        'min_percentage': min_percentage,
        'max_percentage': max_percentage,
        'result_status': result_status,
        'user_query': user_query
    }
 
    logger.info(f"User {request.user.id} viewed result list with filters: user_query={user_query}, min_percentage={min_percentage}, max_percentage={max_percentage}, result_status={result_status}")
    return render(request, 'home/results/result_list.html', context)
 
 
@login_required
def result_view(request, pk):
    result = get_object_or_404(Result.objects.select_related('user', 'test'), pk=pk)
    if not request.user.is_authenticated:
        logger.warning(f"Anonymous user attempted access to result {result.pk}")
        return render(request, 'home/error.html', {
            'message': "You must be logged in to view this result."
        }, status=403)
    if not request.user.is_staff and result.user != request.user:
        logger.warning(f"User {request.user.id} attempted unauthorized access to result {result.pk}")
        return render(request, 'home/error.html', {
            'message': "You are not authorized to view this result."
        }, status=403)
 
    logger.info(f"User {request.user.id} viewed result {result.result_id} for user {result.user.user_id}")
    return render(request, 'home/results/result_view.html', {
        'result': result,
        'user': result.user
    })

#Generate test



def build_header_table():
    """Create a table for participant details without exam date."""
    data = [
        ["Name: _____________________________", "Registration ID: _________________"],
        ["Phone Number: ______________________", "Email: __________________________"]
    ]
    table = Table(data, colWidths=[3.5*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    return table

def add_footer(canvas, doc):
    """Add footer with page number and branding."""
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    page_number = f"Page {doc.page}"
    canvas.drawCentredString(letter[0]/2, 0.5*inch, page_number)
    canvas.drawString(1*inch, 0.5*inch, "Techraq Fresher Hiring")
    canvas.restoreState()

@login_required
def generate_test(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        logger.warning(f"Unauthorized access attempt by user {request.user.email if request.user.is_authenticated else 'anonymous'}")
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')

    current_year = datetime.now().year

    test_type = request.POST.get('test_type', request.GET.get('test_type', 'gt')).lower()
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')

    programming_languages = []
    if test_type == 'tt':
        configs = Configuration.objects.filter(key=f'primary_skills_{current_year}', deleted=False)
        if configs.exists():
            programming_languages = [config.value.strip() for config in configs]
        else:
            logger.warning("Programming languages configuration not found")
            messages.warning(request, "Programming languages not configured. Please add them in Configurations.")

    def get_config_value(key, default):
        config = Configuration.objects.filter(key=key, deleted=False).first()
        return int(config.value) if config and config.value.isdigit() else default

    if test_type == 'gt':
        total_key, easy_key, medium_key, hard_key = (
            f'gt_total_questions_{current_year}', f'gt_easy_questions_{current_year}',
            f'gt_medium_questions_{current_year}', f'gt_hard_questions_{current_year}'
        )
    else:
        total_key, easy_key, medium_key, hard_key = (
            f'tt_total_questions_{current_year}', f'tt_easy_questions_{current_year}',
            f'tt_medium_questions_{current_year}', f'tt_hard_questions_{current_year}'
        )

    total_questions = get_config_value(total_key, 0)
    if total_questions == 0 and request.method == 'POST':
        messages.error(request, f"Total questions key ('{total_key}') must be set and greater than 0 in Configurations.")
        return redirect('configuration_list')

    easy_count = get_config_value(easy_key, 0)
    medium_count = get_config_value(medium_key, 0)
    hard_count = get_config_value(hard_key, 0)

    if test_type == 'tt':
        set_count = sum(1 for x in [easy_count, medium_count, hard_count] if x > 0)
        if set_count < 3:
            tt_mcq_total = (total_questions * 6) // 10
            tt_coding_total = total_questions - tt_mcq_total
            tt_mcq_easy = tt_mcq_total // 3
            tt_mcq_medium = tt_mcq_total // 3
            tt_mcq_hard = tt_mcq_total - (tt_mcq_easy + tt_mcq_medium)
            tt_coding_easy = (tt_coding_total * 2) // 4
            tt_coding_medium = (tt_coding_total * 1) // 4
            tt_coding_hard = tt_coding_total - (tt_coding_easy + tt_coding_medium)
        else:
            tt_mcq_easy = (easy_count * 6) // 10
            tt_coding_easy = easy_count - tt_mcq_easy
            tt_mcq_medium = (medium_count * 6) // 10
            tt_coding_medium = medium_count - tt_mcq_medium
            tt_mcq_hard = (hard_count * 6) // 10
            tt_coding_hard = hard_count - tt_mcq_hard
        gt_easy_count, gt_medium_count, gt_hard_count = 0, 0, 0
        logger.debug(f"TT Question Counts: MCQ Easy={tt_mcq_easy}, MCQ Medium={tt_mcq_medium}, MCQ Hard={tt_mcq_hard}, "
                     f"Coding Easy={tt_coding_easy}, Coding Medium={tt_coding_medium}, Coding Hard={tt_coding_hard}")
    else:
        set_count = sum(1 for x in [easy_count, medium_count, hard_count] if x > 0)
        if set_count < 3:
            gt_easy_count = total_questions // 3
            gt_medium_count = total_questions // 3
            gt_hard_count = total_questions - (gt_easy_count + gt_medium_count)
        else:
            gt_easy_count, gt_medium_count, gt_hard_count = easy_count, medium_count, hard_count
        tt_mcq_easy, tt_mcq_medium, tt_mcq_hard = 0, 0, 0
        tt_coding_easy, tt_coding_medium, tt_coding_hard = 0, 0, 0
        logger.debug(f"GT Question Counts: Easy={gt_easy_count}, Medium={gt_medium_count}, Hard={gt_hard_count}")

    if request.method == 'POST':
        form = GenerateTestForm(request.POST, test_type=test_type, configured_total=total_questions, programming_languages=programming_languages)
        if form.is_valid():
            generate_by_difficulty = form.cleaned_data.get('generate_by_difficulty')
            if generate_by_difficulty == 'no':
                manual_easy = form.cleaned_data.get('num_easy')
                manual_medium = form.cleaned_data.get('num_medium')
                manual_hard = form.cleaned_data.get('num_hard')
                if test_type == 'gt':
                    gt_easy_count, gt_medium_count, gt_hard_count = manual_easy, manual_medium, manual_hard
                    logger.debug(f"GT Manual Counts: Easy={gt_easy_count}, Medium={gt_medium_count}, Hard={gt_hard_count}")
                else:
                    tt_mcq_easy = (manual_easy * 6) // 10
                    tt_coding_easy = manual_easy - tt_mcq_easy
                    tt_mcq_medium = (manual_medium * 6) // 10
                    tt_coding_medium = manual_medium - tt_mcq_medium
                    tt_mcq_hard = (manual_hard * 6) // 10
                    tt_coding_hard = manual_hard - tt_mcq_hard
                    logger.debug(f"TT Manual Counts: MCQ Easy={tt_mcq_easy}, MCQ Medium={tt_mcq_medium}, MCQ Hard={tt_mcq_hard}, "
                                 f"Coding Easy={tt_coding_easy}, Coding Medium={tt_coding_medium}, Coding Hard={tt_coding_hard}")

            try:
                num_sets = form.cleaned_data['num_sets']
                selected_language = form.cleaned_data.get('programming_language') if test_type == 'tt' else None

                # Validate question availability
                if test_type == 'gt':
                    gt_easy = list(Question.objects.filter(test_type='GT', difficulty='easy', is_active=True))
                    gt_medium = list(Question.objects.filter(test_type='GT', difficulty='medium', is_active=True))
                    gt_hard = list(Question.objects.filter(test_type='GT', difficulty='hard', is_active=True))
                    if len(gt_easy) < gt_easy_count or len(gt_medium) < gt_medium_count or len(gt_hard) < gt_hard_count:
                        messages.error(request, f"Insufficient questions in database. Need at least {gt_easy_count} Easy, {gt_medium_count} Medium, and {gt_hard_count} Hard General Test questions.")
                        return redirect(reverse('generate_test') + f'?test_type=gt')
                    logger.debug(f"GT Questions Available: Easy={len(gt_easy)}, Medium={len(gt_medium)}, Hard={len(gt_hard)}")
                else:
                    tt_mcq_easy_qs = list(Question.objects.filter(test_type='TT', specialisation_name=selected_language, difficulty='easy', is_multichoice=True, is_active=True))
                    tt_mcq_medium_qs = list(Question.objects.filter(test_type='TT', specialisation_name=selected_language, difficulty='medium', is_multichoice=True, is_active=True))
                    tt_mcq_hard_qs = list(Question.objects.filter(test_type='TT', specialisation_name=selected_language, difficulty='hard', is_multichoice=True, is_active=True))
                    tt_coding_easy_qs = list(Question.objects.filter(test_type='TT', specialisation_name=selected_language, difficulty='easy', is_multichoice=False, is_active=True))
                    tt_coding_medium_qs = list(Question.objects.filter(test_type='TT', specialisation_name=selected_language, difficulty='medium', is_multichoice=False, is_active=True))
                    tt_coding_hard_qs = list(Question.objects.filter(test_type='TT', specialisation_name=selected_language, difficulty='hard', is_multichoice=False, is_active=True))
                    if (len(tt_mcq_easy_qs) < tt_mcq_easy or len(tt_mcq_medium_qs) < tt_mcq_medium or len(tt_mcq_hard_qs) < tt_mcq_hard or
                        len(tt_coding_easy_qs) < tt_coding_easy or len(tt_coding_medium_qs) < tt_coding_medium or len(tt_coding_hard_qs) < tt_coding_hard):
                        messages.error(request, f"Insufficient questions for {selected_language}. Need at least "
                                               f"MCQ: Easy={tt_mcq_easy}, Medium={tt_mcq_medium}, Hard={tt_mcq_hard}; "
                                               f"Coding: Easy={tt_coding_easy}, Medium={tt_coding_medium}, Hard={tt_coding_hard}.")
                        return redirect(reverse('generate_test') + f'?test_type=tt')
                    logger.debug(f"TT Questions Available for {selected_language}: "
                                 f"MCQ Easy={len(tt_mcq_easy_qs)}, MCQ Medium={len(tt_mcq_medium_qs)}, MCQ Hard={len(tt_mcq_hard_qs)}, "
                                 f"Coding Easy={len(tt_coding_easy_qs)}, Coding Medium={len(tt_coding_medium_qs)}, Coding Hard={len(tt_coding_hard_qs)}")

                # PDF Generation
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                batch_id = timestamp
                pdf_dir = os.path.join(settings.MEDIA_ROOT, 'test_pdfs')
                os.makedirs(pdf_dir, exist_ok=True)

                # Define custom styles
                styles = getSampleStyleSheet()
                styles.add(ParagraphStyle(name='Header', fontName='Helvetica-Bold', fontSize=16, leading=20, alignment=1, spaceAfter=12))
                styles.add(ParagraphStyle(name='SubHeader', fontName='Helvetica', fontSize=12, leading=14, alignment=1, spaceAfter=12))
                styles.add(ParagraphStyle(name='Section', fontName='Helvetica-Bold', fontSize=14, leading=16, spaceBefore=12, spaceAfter=8))
                styles.add(ParagraphStyle(name='Question', fontName='Helvetica-Bold', fontSize=11, leading=14, spaceBefore=8, spaceAfter=4))
                styles.add(ParagraphStyle(name='Option', fontName='Helvetica', fontSize=10, leading=12, leftIndent=20, spaceAfter=2))
                styles.add(ParagraphStyle(name='AnswerSpace', fontName='Helvetica', fontSize=10, leading=12, spaceBefore=4, spaceAfter=4))

                for set_num in range(1, num_sets + 1):
                    pdf_filename = f'set{set_num}_{test_type}_{timestamp}.pdf'
                    pdf_path = os.path.join(pdf_dir, pdf_filename)
                    doc = SimpleDocTemplate(
                        pdf_path,
                        pagesize=letter,
                        leftMargin=1*inch,
                        rightMargin=1*inch,
                        topMargin=1*inch,
                        bottomMargin=1*inch,
                        onFirstPage=add_footer,
                        onLaterPages=add_footer
                    )
                    content = []

                    # First Page: Header, Participant Details, Instructions
                    content.append(Paragraph("Techraq Fresher Hiring", styles['Header']))
                    content.append(Paragraph(
                        f"{'General' if test_type == 'gt' else 'Technical'} Test (Set {set_num})" + 
                        (f" ({selected_language})" if test_type == 'tt' else ""),
                        styles['SubHeader']
                    ))
                    content.append(Spacer(1, 12))
                    content.append(build_header_table())
                    content.append(Spacer(1, 12))
                    if test_type == 'gt':
                        instructions = (
                            "Instructions for General Test:<br/>"
                            "- This test contains multiple-choice questions (MCQs) only.<br/>"
                            "- Select the correct option (A, B, C, or D) for each question.<br/>"
                            "- Each question has exactly one correct answer.<br/>"
                            "- Write your answers on the provided answer sheet.<br/>"
                            "- Ensure all answers are clearly marked."
                        )
                    else:
                        instructions = (
                            "Instructions for Technical Test:<br/>"
                            "- This test contains multiple-choice questions (MCQs) and coding questions.<br/>"
                            "- For MCQs, select the correct option (A, B, C, or D).<br/>"
                            "- For coding questions, write your solution in the space provided below each question on the same page.<br/>"
                            "- Ensure your code is clear, well-structured, and includes necessary comments.<br/>"
                            "- Use the answer space provided below each coding question."
                        )
                    content.append(Paragraph(instructions, styles['SubHeader']))
                    content.append(PageBreak())

                    if test_type == 'gt':
                        set_name = f'GeneralTest_Set{set_num}_{timestamp}'
                        selected_easy = random.sample(gt_easy, min(gt_easy_count, len(gt_easy)))
                        selected_medium = random.sample(gt_medium, min(gt_medium_count, len(gt_medium)))
                        selected_hard = random.sample(gt_hard, min(gt_hard_count, len(gt_hard)))

                        def add_shuffled_questions(title, questions, start_index):
                            if not questions:
                                logger.debug(f"No questions for {title}")
                                return start_index
                            content.append(Paragraph(title, styles['Section']))
                            for i, q in enumerate(questions, start_index):
                                content.append(Paragraph(f"Q{i}. {q.question_text}", styles['Question']))
                                option_texts = [q.option_a, q.option_b, q.option_c, q.option_d]
                                random.shuffle(option_texts)
                                labels = ["A.", "B.", "C.", "D."]
                                for j, opt_text in enumerate(option_texts):
                                    content.append(Paragraph(f"{labels[j]} {opt_text}", styles['Option']))
                                content.append(Spacer(1, 8))
                            return start_index + len(questions)

                        question_counter = 1
                        question_counter = add_shuffled_questions("Easy Questions", selected_easy, question_counter)
                        question_counter = add_shuffled_questions("Medium Questions", selected_medium, question_counter)
                        question_counter = add_shuffled_questions("Hard Questions", selected_hard, question_counter)

                        test_instance = GenerateTest.objects.create(set_name=set_name, pdf_file=f'test_pdfs/{pdf_filename}', test_type='GT', batch_id=batch_id)
                        all_questions = selected_easy + selected_medium + selected_hard
                        GenerateTestQuestions.objects.bulk_create([GenerateTestQuestions(generate_test=test_instance, question=q) for q in all_questions])

                    else:  # tt
                        set_name = f'TechnicalTest_{selected_language}_Set{set_num}_{timestamp}'
                        selected_mcq_easy = random.sample(tt_mcq_easy_qs, min(tt_mcq_easy, len(tt_mcq_easy_qs)))
                        selected_mcq_medium = random.sample(tt_mcq_medium_qs, min(tt_mcq_medium, len(tt_mcq_medium_qs)))
                        selected_mcq_hard = random.sample(tt_mcq_hard_qs, min(tt_mcq_hard, len(tt_mcq_hard_qs)))
                        selected_coding_easy = random.sample(tt_coding_easy_qs, min(tt_coding_easy, len(tt_coding_easy_qs)))
                        selected_coding_medium = random.sample(tt_coding_medium_qs, min(tt_coding_medium, len(tt_coding_medium_qs)))
                        selected_coding_hard = random.sample(tt_coding_hard_qs, min(tt_coding_hard, len(tt_coding_hard_qs)))

                        question_counter = 1
                        def add_shuffled_mcqs(title, questions):
                            nonlocal question_counter
                            if not questions:
                                logger.debug(f"No questions for {title}")
                                return
                            content.append(Paragraph(title, styles['Section']))
                            for q in questions:
                                content.append(Paragraph(f"Q{question_counter}. {q.question_text}", styles['Question']))
                                option_texts = [q.option_a, q.option_b, q.option_c, q.option_d]
                                random.shuffle(option_texts)
                                labels = ["A.", "B.", "C.", "D."]
                                for j, opt_text in enumerate(option_texts):
                                    content.append(Paragraph(f"{labels[j]} {opt_text}", styles['Option']))
                                content.append(Spacer(1, 8))
                                question_counter += 1

                        def add_coding_questions(title, questions):
                            nonlocal question_counter
                            if not questions:
                                logger.debug(f"No questions for {title}")
                                return
                            content.append(Paragraph(title, styles['Section']))
                            for q in questions:
                                # Estimate space for question and instruction
                                question_flowable = Paragraph(f"Q{question_counter}. {q.question_text}", styles['Question'])
                                instruction_flowable = Paragraph("Write your answer below", styles['AnswerSpace'])
                                # Approximate height: 14pt (question leading) + 12pt (instruction leading) + 8pt (spacer) + 36pt (footer)
                                remaining_height = 636 - (14 + 12 + 8 + 36)  # ~566 points = 7.86 inches
                                content.append(question_flowable)
                                content.append(Spacer(1, 4))
                                content.append(instruction_flowable)
                                content.append(Spacer(1, 4))
                                # Use KeepInFrame to ensure the table fits
                                answer_box = Table([[""]], colWidths=[6.5*inch], rowHeights=[7.8*inch], style=[('GRID', (0,0), (-1,-1), 0.5, colors.black)])
                                content.append(KeepInFrame(6.5*inch, 7.8*inch, [answer_box], mode='shrink'))
                                content.append(PageBreak())
                                question_counter += 1

                        add_shuffled_mcqs("Easy Multiple Choice Questions", selected_mcq_easy)
                        add_shuffled_mcqs("Medium Multiple Choice Questions", selected_mcq_medium)
                        add_shuffled_mcqs("Hard Multiple Choice Questions", selected_mcq_hard)
                        add_coding_questions("Easy Coding Questions", selected_coding_easy)
                        add_coding_questions("Medium Coding Questions", selected_coding_medium)
                        add_coding_questions("Hard Coding Questions", selected_coding_hard)

                        test_instance = GenerateTest.objects.create(set_name=set_name, pdf_file=f'test_pdfs/{pdf_filename}', test_type='TT', batch_id=batch_id)
                        all_questions = selected_mcq_easy + selected_mcq_medium + selected_mcq_hard + selected_coding_easy + selected_coding_medium + selected_coding_hard
                        GenerateTestQuestions.objects.bulk_create([GenerateTestQuestions(generate_test=test_instance, question=q) for q in all_questions])

                    doc.build(content)

                messages.success(request, f"Generated {num_sets} {test_type.upper()} test sets successfully!")
                return redirect(reverse('generate_test') + f'?test_type={test_type}')

            except Exception as e:
                logger.error(f"Error generating tests: {e}", exc_info=True)
                messages.error(request, f"An error occurred while generating tests: {e}")

    else:
        form = GenerateTestForm(test_type=test_type, configured_total=total_questions, programming_languages=programming_languages)

    sets = GenerateTest.objects.filter(test_type=test_type.upper()).order_by('-created_at')
    if search_query:
        sets = sets.filter(set_name__icontains=search_query)
    paginator = Paginator(sets, 10)
    page_obj = paginator.get_page(page_number)
    
    # Format the set name for display purposes
    for test_set in page_obj:
        try:
            parts = test_set.set_name.split('_')
            # Check if name has date and time parts (YYYYMMDD_HHMMSS)
            if len(parts) >= 3 and len(parts[-2]) == 8 and parts[-2].isdigit() and len(parts[-1]) == 6 and parts[-1].isdigit():
                date_str = parts[-2]
                time_str = parts[-1]
                
                # Format date: 20250825 -> 2025/08/25
                formatted_date = f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:]}"
                
                # Format time: 185051 -> 18-50-51
                formatted_time = f"{time_str[:2]}-{time_str[2:4]}-{time_str[4:]}"
                
                base_name = "_".join(parts[:-2])
                test_set.formatted_name = f"{base_name}_{formatted_date}_{formatted_time}"
            else:
                test_set.formatted_name = test_set.set_name
        except Exception:
            # Fallback in case of any parsing error
            test_set.formatted_name = test_set.set_name

    context = {
        'form': form,
        'page_obj': page_obj,
        'test_type': test_type,
        'programming_languages': programming_languages,
        'search_query': search_query,
        'configured_total': total_questions,
    }
    return render(request, 'home/tests/generate_test.html', context)

@login_required
def generate_answer_pdf(request, pk):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('login')

    try:
        test_set = get_object_or_404(GenerateTest, pk=pk)
        if test_set.test_type != 'GT':
            messages.error(request, "Answer sheets are only available for General Tests.")
            return redirect(reverse('generate_test') + '?test_type=gt')
        
        # Fetch questions grouped by difficulty
        easy_questions = Question.objects.filter(
            generatetestquestions__generate_test=test_set, difficulty='easy'
        ).order_by('question_id')
        medium_questions = Question.objects.filter(
            generatetestquestions__generate_test=test_set, difficulty='medium'
        ).order_by('question_id')
        hard_questions = Question.objects.filter(
            generatetestquestions__generate_test=test_set, difficulty='hard'
        ).order_by('question_id')

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=1*inch,
            rightMargin=1*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Header', fontName='Helvetica-Bold', fontSize=16, alignment=1, spaceAfter=24))
        styles.add(ParagraphStyle(name='Section', fontName='Helvetica-Bold', fontSize=14, leading=16, spaceBefore=18, spaceAfter=6, textColor=colors.darkblue))
        styles.add(ParagraphStyle(name='Question', fontName='Helvetica-Bold', fontSize=11, leading=14, spaceBefore=12, spaceAfter=4))
        styles.add(ParagraphStyle(name='Answer', fontName='Helvetica-Bold', fontSize=10, leading=12, leftIndent=20, spaceAfter=8, textColor=colors.darkgreen))

        content = []
        # Display the formatted name in the PDF header
        try:
            parts = test_set.set_name.split('_')
            date_str, time_str = parts[-2], parts[-1]
            formatted_date = f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:]}"
            formatted_time = f"{time_str[:2]}-{time_str[2:4]}-{time_str[4:]}"
            base_name = "_".join(parts[:-2])
            formatted_name = f"{base_name}_{formatted_date}_{formatted_time}"
        except Exception:
            formatted_name = test_set.set_name # Fallback
        
        content.append(Paragraph(f"Answer Key for: {formatted_name}", styles['Header']))

        question_counter = 1

        def add_answers_section(title, questions):
            nonlocal question_counter
            if questions.exists():
                # << CHANGE: Wrap title in <u> tags for underline >>
                content.append(Paragraph(f"<u>{title}</u>", styles['Section']))
                for q in questions:
                    content.append(Paragraph(f"Q{question_counter}. {q.question_text}", styles['Question']))
                    options = {'A': q.option_a, 'B': q.option_b, 'C': q.option_c, 'D': q.option_d}
                    correct_option_text = options.get(q.correct_answer, "N/A")
                    content.append(Paragraph(f"Correct Answer: {q.correct_answer}. {correct_option_text}", styles['Answer']))
                    question_counter += 1
        
        # Add questions section by section with underlined, colored headings
        add_answers_section("Easy Questions and Answers", easy_questions)
        add_answers_section("Medium Questions and Answers", medium_questions)
        add_answers_section("Hard Questions and Answers", hard_questions)
        
        doc.build(content)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="answers_{test_set.set_name}.pdf"'
        return response

    except Exception as e:
        logger.error(f"Error generating answer PDF for set {pk}: {e}", exc_info=True)
        messages.error(request, f"An error occurred while generating the answer PDF: {e}")
        return redirect(reverse('generate_test') + '?test_type=gt')

# ... (rest of your views.py file from download_test_sets_zip to the end) ...
@login_required
def download_test_sets_zip(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        logger.warning(f"Unauthorized access attempt by user {request.user.email if request.user.is_authenticated else 'anonymous'}")
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')
 
    try:
        latest_batch_id = request.session.get('latest_batch_id', None)
        test_type = request.GET.get('test_type', None)
 
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            if test_type:
                sets = GenerateTest.objects.filter(batch_id=latest_batch_id, test_type=test_type.upper()) if latest_batch_id else GenerateTest.objects.filter(test_type=test_type.upper())
            else:
                sets = GenerateTest.objects.filter(batch_id=latest_batch_id) if latest_batch_id else GenerateTest.objects.all()
 
            for test_set in sets:
                pdf_path = os.path.join(settings.MEDIA_ROOT, test_set.pdf_file.name)
                if os.path.exists(pdf_path):
                    if test_type:
                        zip_file.write(pdf_path, os.path.basename(pdf_path))
                    else:
                        folder = 'General_Test_Sets' if test_set.test_type == 'GT' else 'Technical_Test_Sets'
                        zip_file.write(pdf_path, os.path.join(folder, os.path.basename(pdf_path)))
 
        zip_buffer.seek(0)
 
        if test_type:
            zip_name = f'TechRaq_{test_type.upper()}_Sets_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        else:
            zip_name = f'TechRaq_All_Test_Sets_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
 
        logger.info(f"Downloaded ZIP for user {request.user.email} (batch {latest_batch_id or 'all'}, type {test_type or 'all'})")
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={zip_name}'
        return response
 
    except Exception as e:
        logger.error(f"Error generating ZIP: {str(e)}")
        messages.error(request, "An error occurred while generating the ZIP file.")
        test_type = request.GET.get('test_type', 'gt').lower()
        return redirect(f"{reverse('generate_test')}?test_type={test_type}")
 
class ConfigurationListView(LoginRequiredMixin, ListView):
    model = Configuration
    template_name = 'home/configurations/configuration_list.html'
    context_object_name = 'configurations'
    paginate_by = 10
 
    def get_queryset(self):
        queryset = super().get_queryset()
        key_query = self.request.GET.get('key_query')
        if key_query:
            queryset = queryset.filter(key__icontains=key_query)
        return queryset.filter(deleted=False).order_by('-created_date')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key_query'] = self.request.GET.get('key_query', '')
 
        config_ids = [config.configID for config in context['configurations'] if config.configID]
        config_keys_mapping = {
            str(config_key.id): config_key.values
            for config_key in ConfigKeys.objects.filter(id__in=config_ids, deleted=True)
        }
 
        for config in context['configurations']:
            config.display_key = config_keys_mapping.get(config.configID, config.key)
 
        return context
 
class ConfigurationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Configuration
    form_class = ConfigurationForm
    template_name = 'home/configurations/configuration_form.html'
    success_url = reverse_lazy('configuration_list')
    success_message = "Configuration was created successfully"
 
class ConfigurationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Configuration
    form_class = ConfigurationForm
    template_name = 'home/configurations/configuration_form.html'
    success_url = reverse_lazy('configuration_list')
    success_message = "Configuration was updated successfully"
 
class ConfigurationDeleteView(LoginRequiredMixin, DeleteView):
    model = Configuration
    template_name = 'home/configurations/configuration_confirm_delete.html'
    success_url = reverse_lazy('configuration_list')
 
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted = True
        self.object.save()
        messages.success(request, "Configuration was deleted successfully")
        return redirect(self.success_url)
@login_required
def export_users(request):
    # Handle both GET and POST (keeping POST for backward compatibility)
    query = request.GET.get('q') or request.POST.get('q')
    from_date = request.GET.get('from_date') or request.POST.get('from_date')
    to_date = request.GET.get('to_date') or request.POST.get('to_date')
    
    try:
        # Start with base queryset
        users = Users.objects.filter(deleted=False)
        
        # Apply filters if provided
        if query:
            users = users.filter(
                Q(mobile__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(registration_id__icontains=query)
            )
        
        if from_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
                users = users.filter(registered_at__gte=from_date)
            except ValueError:
                pass  # Ignore invalid date format
        
        if to_date:
            try:
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
                to_date = to_date.replace(hour=23, minute=59, second=59)
                users = users.filter(registered_at__lte=to_date)
            except ValueError:
                pass  # Ignore invalid date format
        
        # Define specific fields to export
        export_fields = [
            'user_id',
            'registration_id',
            'first_name',
            'last_name',
            'gender',
            'dob',
            'email',
            'action_status',
            'general_test_attendance',
            'general_test_score',
            'general_test_result',
            'technical_test_attendance',
            'technical_test_score',
            'technical_test_result',
            'technical_test_name'
        ]
        
        # Get filtered users data with selected fields, joining with ManualResults
        users_data = users.values(
            'user_id',
            'registration_id',
            'first_name',
            'last_name',
            'gender',
            'dob',
            'email',
            'action_status'
        )
        
        # Get corresponding ManualResults data
        manual_results = ManualResults.objects.filter(user__in=users).values(
            'user_id',
            'general_test_attendance',
            'general_test_score',
            'general_test_result',
            'technical_test_attendance',
            'technical_test_score',
            'technical_test_result',
            'technical_test_name'
        )
        
        # Create DataFrames
        users_df = pd.DataFrame.from_records(users_data)
        results_df = pd.DataFrame.from_records(manual_results)
        
        # Merge DataFrames on user_id
        if not users_df.empty and not results_df.empty:
            df = users_df.merge(
                results_df,
                on='user_id',
                how='left'  # Left join to include users without results
            )
        elif not users_df.empty:
            # If no results, use users data only, fill missing fields with None
            df = users_df
            for field in [
                'general_test_attendance',
                'general_test_score',
                'general_test_result',
                'technical_test_attendance',
                'technical_test_score',
                'technical_test_result',
                'technical_test_name'
            ]:
                df[field] = None
        else:
            # If no users, create empty DataFrame with expected columns
            df = pd.DataFrame(columns=export_fields)
        
        # Ensure all expected columns are present
        for field in export_fields:
            if field not in df.columns:
                df[field] = None
        
        # Reorder columns to match export_fields
        df = df[export_fields]
        
        # Create in-memory file
        output = BytesIO()
        content_type = 'text/csv'
        file_extension = 'csv'
        df.to_csv(output, index=False)
        
        # Prepare response
        output.seek(0)
        response = HttpResponse(
            output.getvalue(),
            content_type=content_type
        )
        response['Content-Disposition'] = f'attachment; filename=users_export.{file_extension}'
        return response
        
    except Exception as e:
        messages.error(request, f"Export failed: {str(e)}")
        return redirect('user_list')

logger = logging.getLogger(__name__)

def import_status(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            file = request.FILES['file']

            if not file.name.endswith(('.csv', '.xlsx')):
                messages.error(request, "Please upload a valid CSV or Excel file.")
                return redirect('user_list')

            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            expected_columns = [
                'user_id', 'registration_id', 
                'general_test_attendance', 'general_test_score', 'general_test_result',
                'technical_test_attendance', 'technical_test_score', 'technical_test_result',
                'technical_test_name', 'action_status'
            ]

            # Check for missing columns
            if not all(col in df.columns for col in expected_columns):
                missing_cols = [col for col in expected_columns if col not in df.columns]
                messages.error(request, f"Missing required columns: {', '.join(missing_cols)}")
                return redirect('user_list')

            valid_yes_no_choices = ['Yes', 'No']
            valid_pass_fail_choices = ['Pass', 'Fail', 'N/A']

            updated_count = 0
            for _, row in df.iterrows():
                try:
                    user_id = str(row['user_id']).strip()
                    registration_id = str(row['registration_id']).strip()
                    if not user_id or not registration_id:
                        logger.warning("Empty user_id or registration_id found in row.")
                        continue

                    # Verify user exists with matching user_id and registration_id
                    user = Users.objects.filter(user_id=user_id, registration_id=registration_id).first()
                    if not user:
                        logger.warning(f"No user found with user_id: {user_id} and registration_id: {registration_id}")
                        continue

                    general_attendance = str(row['general_test_attendance']).strip().capitalize()
                    general_result = str(row['general_test_result']).strip().capitalize()
                    technical_attendance = str(row['technical_test_attendance']).strip().capitalize()
                    technical_result = str(row['technical_test_result']).strip().capitalize()

                    if general_attendance not in valid_yes_no_choices:
                        logger.warning(f"Invalid general_test_attendance '{general_attendance}' for user_id: {user_id}")
                        continue
                    if general_result not in valid_pass_fail_choices:
                        logger.warning(f"Invalid general_test_result '{general_result}' for user_id: {user_id}")
                        continue
                    if technical_attendance not in valid_yes_no_choices:
                        logger.warning(f"Invalid technical_test_attendance '{technical_attendance}' for user_id: {user_id}")
                        continue
                    if technical_result not in valid_pass_fail_choices:
                        logger.warning(f"Invalid technical_test_result '{technical_result}' for user_id: {user_id}")
                        continue

                    # Validate score fields
                    general_score = row['general_test_score']
                    if pd.notnull(general_score):
                        try:
                            general_score = float(general_score)
                            if not (0 <= general_score <= 100):
                                logger.warning(f"Invalid general_test_score '{general_score}' for user_id: {user_id}")
                                continue
                        except (ValueError, TypeError):
                            logger.warning(f"Invalid general_test_score format for user_id: {user_id}")
                            continue
                    else:
                        general_score = None

                    technical_score = row['technical_test_score']
                    if pd.notnull(technical_score):
                        try:
                            technical_score = float(technical_score)
                            if not (0 <= technical_score <= 100):
                                logger.warning(f"Invalid technical_test_score '{technical_score}' for user_id: {user_id}")
                                continue
                        except (ValueError, TypeError):
                            logger.warning(f"Invalid technical_test_score format for user_id: {user_id}")
                            continue
                    else:
                        technical_score = None

                    # Update action_status in Users model
                    user.action_status = str(row['action_status']).strip()
                    user.save()

                    # Update or create ManualResults record
                    manual_result, created = ManualResults.objects.update_or_create(
                        user=user,
                        registration_id=user,
                        defaults={
                            'general_test_attendance': general_attendance,
                            'general_test_score': general_score,
                            'general_test_result': general_result,
                            'technical_test_attendance': technical_attendance,
                            'technical_test_score': technical_score,
                            'technical_test_result': technical_result,
                            'technical_test_name': str(row['technical_test_name']).strip()
                        }
                    )
                    updated_count += 1

                except Exception as row_err:
                    logger.error(f"Error updating user {row.get('user_id', '[unknown]')}: {row_err}")
                    continue

            messages.success(request, f"Successfully updated {updated_count} user(s).")
            return redirect('user_list')

        except Exception as e:
            logger.error(f"Import failed: {str(e)}")
            messages.error(request, f"Import failed: {str(e)}")
            return redirect('user_list')

    messages.error(request, "No file uploaded or invalid request method.")
    return redirect('user_list')


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    total_users = Users.objects.filter(deleted=False).count()
    total_questions = Question.objects.filter(deleted=False).count()
    total_tests = Tests.objects.filter(is_submitted=1).count()
    total_results = Result.objects.count()
    avg_percentage = Result.objects.aggregate(avg=Avg('percentage'))['avg']
    pass_percentage = round(avg_percentage, 2) if avg_percentage else 0

    # General Test Data
    gt_attended = Tests.objects.filter(test_type='GT', is_submitted=True).count()
    gt_results = Result.objects.filter(test__test_type='GT')
    gt_qualified = gt_results.filter(result_status='pass').count()
    gt_not_qualified = gt_results.filter(result_status='fail').count()

    # Technical Test Data
    tt_attended = Tests.objects.filter(test_type='TT', is_submitted=True).count()
    tt_results = Result.objects.filter(test__test_type='TT')
    tt_qualified = tt_results.filter(result_status='pass').count()
    tt_not_qualified = tt_results.filter(result_status='fail').count()

    # Skills vs Qualified
    skills_data = Result.objects.filter(result_status='pass')\
        .values('skill').annotate(count=Count('result_id'))\
        .order_by('-count')[:5]

    # Fallback for empty skills data
    if not skills_data:
        skills_data = [{'skill': 'No Skills Data', 'count': 0}]

    context = {
        'total_users': total_users,
        'total_questions': total_questions,
        'total_tests': total_tests,
        'total_results': total_results,
        'pass_percentage': pass_percentage,
        'gt_data': {
            'labels': json.dumps(['Attended', 'Qualified', 'Not Qualified']),
            'data': json.dumps([gt_attended, gt_qualified, gt_not_qualified])
        },
        'tt_data': {
            'labels': json.dumps(['Attended', 'Qualified', 'Not Qualified']),
            'data': json.dumps([tt_attended, tt_qualified, tt_not_qualified])
        },
        'skills_chart': {
            'labels': json.dumps([item['skill'] for item in skills_data if item['skill']]),
            'data': json.dumps([item['count'] for item in skills_data if item['skill']])
        }
    }

    return render(request, 'admin/index.html', context)

@login_required
def final_result_list(request):
   
 
    # Get all final results
    final_results = FinalResult.objects.select_related('user').all()
 
    # Search and filter
    user_query = request.GET.get('user_query', '').strip()
    result_status = request.GET.get('result_status', '').strip().lower()
    technical_skill = request.GET.get('technical_skill', '').strip()
    is_published = request.GET.get('is_published', '').strip().lower()
 
    if user_query:
        final_results = final_results.filter(
            Q(user__first_name__icontains=user_query) |
            Q(user__last_name__icontains=user_query)|
            Q(user__registration_id__icontains=user_query)
        )
 
    if result_status in ['pass', 'fail']:
        final_results = final_results.filter(result_status=result_status)
 
    # Filter by Technical Test Skill
    if technical_skill:
        # Get users who have a TT result with the selected skill
        tt_users = Result.objects.filter(
            test__test_type='TT',
            skill=technical_skill
        ).values_list('user_id', flat=True)
        final_results = final_results.filter(user_id__in=tt_users)
 
    # Filter by Published/Not Published
    if is_published in ['true', 'false']:
        is_published_bool = is_published == 'true'
        final_results = final_results.filter(is_result_published=is_published_bool)
 
    # Sort by final_result_id in descending order
    final_results = final_results.order_by('-final_result_id')
    paginator = Paginator(final_results, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
 
    # Prepare data for each result (First Name, Last Name, GT Correct Answers, TT Skill, TT Correct Answers, Result Status, Is Result Published)
    results_with_scores = []
    for result in page_obj:
        gt_result = Result.objects.filter(user=result.user, test__test_type='GT').order_by('-generated_at').first()
        gt_correct = gt_result.total_correct_answers if gt_result else "N/A"
 
        tt_result = Result.objects.filter(user=result.user, test__test_type='TT').order_by('-generated_at').first()
        tt_correct = tt_result.total_correct_answers if tt_result else "N/A"
        tt_skill = tt_result.skill if tt_result and tt_result.skill else "N/A"
 
        results_with_scores.append({
            'result': result,
            'gt_correct': gt_correct,
            'tt_correct': tt_correct,
            'tt_skill': tt_skill,
        })
 
    # Get unique technical skills for the filter dropdown
    technical_skills = Result.objects.filter(
        test__test_type='TT'
    ).values_list('skill', flat=True).distinct().exclude(skill__isnull=True).exclude(skill='')
 
    logger.info(f"User {request.user.id} viewed final result list with {final_results.count()} results")
    return render(request, 'home/final_results/list.html', {
        'page_obj': page_obj,
        'results_with_scores': results_with_scores,
        'technical_skills': technical_skills,
    })
 
@login_required
def final_result_view(request, final_result_id):
    # Authorization check removed as per request; @login_required ensures user is authenticated
    # Add alternative authorization logic here if needed in the future
 
    final_result = get_object_or_404(FinalResult, final_result_id=final_result_id)
    gt_result = Result.objects.filter(user=final_result.user, test__test_type='GT').order_by('-generated_at').first()
    tt_result = Result.objects.filter(user=final_result.user, test__test_type='TT').order_by('-generated_at').first()
 
    logger.info(f"User {request.user.id} viewed final result {final_result.final_result_id} for user {final_result.user.email}")
    return render(request, 'home/final_results/view.html', {
        'final_result': final_result,
        'gt_result': gt_result,
        'tt_result': tt_result,
    })
 
@login_required
def final_result_edit(request, final_result_id):
    # Authorization check removed as per request; @login_required ensures user is authenticated
    # Add alternative authorization logic here if needed in the future
 
    final_result = get_object_or_404(FinalResult, final_result_id=final_result_id)
    gt_result = Result.objects.filter(user=final_result.user, test__test_type='GT').order_by('-generated_at').first()
    tt_result = Result.objects.filter(user=final_result.user, test__test_type='TT').order_by('-generated_at').first()
 
    if request.method == 'POST':
        form = FinalResultForm(request.POST, instance=final_result)
        if form.is_valid():
            final_result = form.save(commit=False)
            final_result.save()
            logger.info(f"Final result updated for user {final_result.user.email}: {final_result.result_status}")
            messages.success(request, "Final result updated successfully.")
            return redirect('final_result_list')
    else:
        form = FinalResultForm(instance=final_result)
 
    return render(request, 'home/final_results/edit.html', {
        'form': form,
        'final_result': final_result,
        'gt_result': gt_result,
        'tt_result': tt_result,
    })
 
@login_required
def final_result_graphs(request):
    # Aggregate counts of pass and fail statuses for FinalResult
    result_counts = FinalResult.objects.values('result_status').annotate(count=Count('result_status'))
   
    # Calculate total attended (total FinalResult records)
    attended_count = FinalResult.objects.count()
 
    # Initialize counts with 0 to avoid None values
    qualified_count = 0
    not_qualified_count = 0
 
    # Extract counts from the query
    for result in result_counts:
        if result['result_status'].lower() == 'pass':
            qualified_count = result['count'] or 0
        elif result['result_status'].lower() == 'fail':
            not_qualified_count = result['count'] or 0
 
    # Calculate GT Attended, Qualified, and Not Qualified counts
    gt_results = Result.objects.filter(test__test_type='GT')
    gt_attended_count = gt_results.count()
    gt_counts = gt_results.values('result_status').annotate(count=Count('result_status'))
    gt_qualified_count = 0
    gt_not_qualified_count = 0
    for gt_result in gt_counts:
        if gt_result['result_status'].lower() == 'pass':
            gt_qualified_count = gt_result['count'] or 0
        elif gt_result['result_status'].lower() == 'fail':
            gt_not_qualified_count = gt_result['count'] or 0
 
    # Calculate TT Attended and skill-based Qualified/Not Qualified counts
    tt_results = Result.objects.filter(test__test_type='TT')
    tt_attended_count = tt_results.count()
    tt_counts = tt_results.values('skill', 'result_status').annotate(count=Count('result_status')).order_by('skill')
    tt_by_skill = {}
    for tt_result in tt_counts:
        skill = tt_result['skill'] or 'Unknown Skill'
        if skill not in tt_by_skill:
            tt_by_skill[skill] = {'qualified': 0, 'not_qualified': 0}
        if tt_result['result_status'].lower() == 'pass':
            tt_by_skill[skill]['qualified'] = tt_result['count'] or 0
        elif tt_result['result_status'].lower() == 'fail':
            tt_by_skill[skill]['not_qualified'] = tt_result['count'] or 0
 
    logger.info(f"User {request.user.id} viewed final result graphs: Attended={attended_count}, Qualified={qualified_count}, Not Qualified={not_qualified_count}, GT Attended={gt_attended_count}, GT Qualified={gt_qualified_count}, GT Not Qualified={gt_not_qualified_count}, TT Attended={tt_attended_count}, TT by Skill={tt_by_skill}")
    return render(request, 'home/final_results/graphs.html', {
        'attended_count': attended_count,
        'qualified_count': qualified_count,
        'not_qualified_count': not_qualified_count,
        'gt_attended_count': gt_attended_count,
        'gt_qualified_count': gt_qualified_count,
        'gt_not_qualified_count': gt_not_qualified_count,
        'tt_attended_count': tt_attended_count,
        'tt_by_skill': tt_by_skill,
    })
 
@login_required
def send_result_email(request, final_result_id):
    # Authorization check removed as per request; @login_required ensures user is authenticated
    # Add alternative authorization logic here if needed in the future
 
    final_result = get_object_or_404(FinalResult, final_result_id=final_result_id)
 
    # Send email to the user
    try:
        # Set subject to "Exam Result" for both pass and fail
        subject = "Exam Result"
 
        # Set message based on result_status
        if final_result.result_status.lower() == 'pass':
            message = (
                f"Dear {final_result.user.full_name or 'User'},\n\n"
                f"You have cleared the first round of assessment and wait for next information from us.\n\n"
                f"Best regards,\nRecruitment Team"
            )
        else:
            message = (
                f"Dear {final_result.user.full_name or 'User'},\n\n"
                f"You have not cleared the first round of assessment. Thank you for your participation.\n\n"
                f"Best regards,\nRecruitment Team"
            )
 
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [final_result.user.email],
            fail_silently=False,
        )
 
        # Update is_result_published to True after sending the email
        final_result.is_result_published = True
        final_result.save()
 
        logger.info(f"Email sent to {final_result.user.email} for final result {final_result.final_result_id}, is_result_published set to True")
        messages.success(request, f"An email has been sent to {final_result.user.email}.")
    except Exception as e:
        logger.error(f"Failed to send email to {final_result.user.email}: {str(e)}")
        messages.error(request, "Failed to send email to the user.")
 
    return redirect('final_result_list')