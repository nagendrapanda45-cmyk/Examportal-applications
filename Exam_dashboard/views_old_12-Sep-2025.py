from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib import messages
from home.users.models import Tests, TestUserQuestionAnswer, Users, Result, Question, Configuration, Instruction
from django.http import JsonResponse, HttpResponseForbidden,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, datetime
from functools import wraps
import base64
import os
import random


# Global
current_year = datetime.now().year


# ------------------------ Helpers ------------------------

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('user_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def get_config_key_with_year(key):
    return f"{key}_{datetime.now().year}"


def get_config_value(key, default=None, cast_type=None):
    """Fetch config by key, falling back to non-year variant"""
    try:
        config_key = get_config_key_with_year(key)
        config = Configuration.objects.get(key=config_key, deleted=False)
    except Configuration.DoesNotExist:
        try:
            config = Configuration.objects.get(key=key, deleted=False)
        except Configuration.DoesNotExist:
            return default
    try:
        return cast_type(config.value) if cast_type else config.value
    except Exception:
        return default


# ------------------------ Suspicious Activity ------------------------

@csrf_exempt
def update_suspicious_activity(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    test_id = request.session.get('test_id')
    person_count = int(request.POST.get('person_count', 0))
    try:
        test = Tests.objects.get(test_id=test_id, user__user_id=request.session.get('user_id'))
        freeze_popup = auto_submit = False

        if person_count == 0 or person_count > 1:
            test.suspicious_activity_count += 1
            test.save()

            freeze_threshold = get_config_value('suspicious_activity_majorpopup', 3, int)
            max_freeze_count = get_config_value('suspicious_activity_count', 9, int)

            if test.suspicious_activity_count % freeze_threshold == 0 and test.suspicious_activity_count < max_freeze_count:
                freeze_popup = True
            if test.suspicious_activity_count >= max_freeze_count:
                auto_submit = True

        return JsonResponse({
            'status': 'success',
            'suspicious_activity_count': test.suspicious_activity_count,
            'freeze_popup': freeze_popup,
            'auto_submit': auto_submit,
            'freeze_timer': get_config_value('freeze_Major_popup_timesec', 50, int)
        })
    except Tests.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Test not found'}, status=404)


# ------------------------ General Test ------------------------

@login_required
def start_test(request):

    # Device restriction
    ua = request.user_agent
    if ua.is_mobile or ua.is_tablet:
        return HttpResponseForbidden("Exams can only be taken on a Desktop device.")
    if ua.browser.family not in ["Chrome", "Firefox", "Edge"]:
        return HttpResponseForbidden("Please use Chrome, Firefox, or Edge on Desktop.")
    
    try:
        user = Users.objects.get(user_id=request.session['user_id'])
    except Users.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found. Please log in again.'})

    # prevent retake
    if Tests.objects.filter(user=user, test_type='GT', is_submitted=True).exists():
        messages.info(request, 'You have already completed and submitted the General Test.')
        return redirect('test_selection')

    # resume active test if exists
    try:
        active_tests = Tests.objects.filter(user=user, is_submitted=False, test_type='GT').order_by('-start_time')
        if active_tests.exists():
            existing_test = active_tests[0]
            current_time = timezone.now()
            duration_seconds = existing_test.duration_minutes * 60
            time_spent = (existing_test.submission_time or current_time) - existing_test.start_time
            remaining_seconds = max(0, duration_seconds - time_spent.total_seconds())

            if remaining_seconds <= 0:
                # auto submit
                existing_test.is_active = False
                existing_test.is_submitted = True
                existing_test.submission_time = current_time
                existing_test.test_status = 2
                existing_test.save()

                answers = TestUserQuestionAnswer.objects.filter(test=existing_test)
                total_questions = get_config_value('gt_total_questions', 30, int)
                total_correct = answers.filter(is_correct=True).count()
                total_attempted = answers.exclude(user_answer='').count()
                percentage = (total_correct / total_questions * 100) if total_questions else 0
                cutoff = get_config_value('gt_cutoff_pass_score', 15, int)
                result_status = 'pass' if total_correct >= cutoff else 'fail'
                Result.objects.update_or_create(
                    test=existing_test, user=user,
                    defaults=dict(
                        total_questions=total_questions,
                        total_attempted_questions=total_attempted,
                        total_correct_answers=total_correct,
                        percentage=percentage,
                        cutoff_pass_score=cutoff,
                        result_status=result_status
                    )
                )
                messages.info(request, 'Previous test expired and was auto-submitted.')
                return redirect('test_selection')

            # resume state
            existing_test.test_status = 1
            existing_test.save()
            request.session.update({
                'test_id': existing_test.test_id,
                'question_ids': list(TestUserQuestionAnswer.objects.filter(test=existing_test)
                                     .order_by('attempt_id')
                                     .values_list('question__question_id', flat=True)),
                'current_index': max(0, min(request.session.get('current_index', 0),
                                            TestUserQuestionAnswer.objects.filter(test=existing_test).count() - 1)),
                'answers': {str(i): qa.user_answer for i, qa in enumerate(
                    TestUserQuestionAnswer.objects.filter(test=existing_test)) if qa.user_answer},
                'marked_for_review': {str(i): qa.status == 'review' for i, qa in enumerate(
                    TestUserQuestionAnswer.objects.filter(test=existing_test))},
                'start_time': current_time.timestamp(),
                'remaining_seconds': remaining_seconds,
                'original_start_time': existing_test.start_time.timestamp()
            })
            request.session.modified = True
            return redirect('test_page', question_index=request.session['current_index'])
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error resuming test: {e}'})

    # start new test
    for k in ['test_id', 'question_ids', 'current_index', 'answers',
              'marked_for_review', 'start_time', 'remaining_seconds', 'original_start_time']:
        request.session.pop(k, None)

    try:
        # fetch question pools
        easy_qs = list(Question.objects.filter(test_type='GT', difficulty='easy', is_active=True))
        med_qs = list(Question.objects.filter(test_type='GT', difficulty='medium', is_active=True))
        hard_qs = list(Question.objects.filter(test_type='GT', difficulty='hard', is_active=True))
        easy_count = get_config_value('gt_easy_questions', 10, int)
        med_count = get_config_value('gt_medium_questions', 10, int)
        hard_count = get_config_value('gt_hard_questions', 10, int)

        if len(easy_qs) < easy_count or len(med_qs) < med_count or len(hard_qs) < hard_count:
            return render(request, 'error.html', {'message': 'Not enough questions to start the test.'})

        selected_questions = (
            random.sample(easy_qs, easy_count) +
            random.sample(med_qs, med_count) +
            random.sample(hard_qs, hard_count)
        )
        random.shuffle(selected_questions)

        duration = get_config_value('gt_duration_minutes', 30, int)
        test = Tests.objects.create(
            user=user, test_name="General Test", test_type='GT',
            duration_minutes=duration, start_time=timezone.now(),
            end_time=timezone.now() + timedelta(minutes=duration),
            is_active=True, is_submitted=False, suspicious_activity_count=0, test_status=1,
        )

        for q in selected_questions:
            TestUserQuestionAnswer.objects.create(
                user=user, test=test, question=q, user_answer='',
                actual_answer=q.correct_answer, is_correct=None, score=0,
                status='not_answered', submitted_at=None, end_time=None,
                option_order='A,B,C,D'
            )

        request.session.update({
            'test_id': test.test_id,
            'question_ids': [q.question_id for q in selected_questions],
            'current_index': 0,
            'answers': {},
            'marked_for_review': {},
            'start_time': test.start_time.timestamp(),
            'remaining_seconds': duration * 60,
            'original_start_time': test.start_time.timestamp()
        })
        request.session.modified = True
        return redirect('test_page', question_index=0)
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error creating new test: {e}'})


@login_required
def test_page(request, question_index):
    
    try:
        user = Users.objects.get(user_id=request.session['user_id'])
    except Users.DoesNotExist:
        return redirect('user_login')

    if 'test_id' not in request.session or 'question_ids' not in request.session:
        return redirect('start_test')

    try:
        test = Tests.objects.get(test_id=request.session['test_id'])
    except Tests.DoesNotExist:
        return render(request, 'error.html', {'message': 'Test not found.'})

    question_ids = request.session['question_ids']
    current_index = int(question_index)

    # Prevent going back
    if current_index < request.session.get('current_index', 0):
        return redirect('test_page', question_index=request.session['current_index'])

    if current_index < 0 or current_index >= len(question_ids):
        return redirect('submit_test')

    try:
        question = Question.objects.get(question_id=question_ids[current_index])
        question_answer, created = TestUserQuestionAnswer.objects.get_or_create(
            user=user, test=test, question=question,
            # defaults={'start_time': timezone.now(), 'option_order': 'A,B,C,D'}
            defaults={'start_time': timezone.now()}
        )
        if not created and not question_answer.start_time:
            question_answer.start_time = timezone.now()
            question_answer.save()
    except Question.DoesNotExist:
        return render(request, 'error.html', {'message': 'Question not found.'})

    instructions = Instruction.objects.filter(test_type='GT', is_active=True).order_by('display_order')

    # Timer
    remaining_seconds = request.session.get('remaining_seconds', test.duration_minutes * 60)
    current_time = timezone.now().timestamp()
    elapsed = current_time - request.session['start_time']
    remaining_seconds = max(0, remaining_seconds - elapsed)
    request.session.update({'remaining_seconds': remaining_seconds, 'start_time': current_time,
                            'current_index': current_index})
    request.session.modified = True
    if remaining_seconds <= 0:
        return redirect('submit_test')

    if request.method == 'POST':
        user_answer = request.POST.get('answer', '')
        mark_review = 'mark_review' in request.POST
        request.session['answers'][str(current_index)] = user_answer
        request.session['marked_for_review'][str(current_index)] = mark_review
        request.session.modified = True
        status = 'review' if mark_review else ('answered' if user_answer else 'not_answered')

        question_answer.user_answer = user_answer
        question_answer.actual_answer = question.correct_answer
        question_answer.is_correct = user_answer == question.correct_answer if user_answer else None
        question_answer.score = 1 if user_answer == question.correct_answer else 0
        question_answer.status = status
        question_answer.submitted_at = timezone.now()
        question_answer.end_time = timezone.now()
        question_answer.save()

        # update prev end_time
        if current_index > 0 and request.POST.get('action') == 'next':
            try:
                prev_q = Question.objects.get(question_id=question_ids[current_index - 1])
                prev_ans = TestUserQuestionAnswer.objects.get(user=user, test=test, question=prev_q)
                if not prev_ans.end_time:
                    prev_ans.end_time = timezone.now()
                    prev_ans.save()
            except Exception:
                pass

        test.is_active = True
        test.save()

        action = request.POST.get('action')
        if action == 'next':
            next_index = current_index + 1
            if next_index < len(question_ids):
                return redirect('test_page', question_index=next_index)
            else:
                return redirect('submit_test')
        elif action == 'prev' and current_index > 0:
            return redirect('test_page', question_index=current_index - 1)
        elif action == 'submit':
            return redirect('submit_test')

    answers = request.session.get('answers', {})
    marked_for_review = request.session.get('marked_for_review', {})
    context = {
        'question': question,
        'current_index': current_index,
        'total_questions': len(question_ids),
        'remaining_time': remaining_seconds,
        'answers': answers,
        'marked_for_review': marked_for_review,
        'question_range': range(len(question_ids)),
        'saved_answer': answers.get(str(current_index), ''),
        'saved_review': marked_for_review.get(str(current_index), False),
        'user': user,
        'options': ['A', 'B', 'C', 'D'],   # fixed order
        'instructions': instructions,
        'test': test,
        'alert_duration': get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
        'alert_cooldown': get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
    }
    return render(request, 'test_page.html', context)


@login_required
def submit_test(request):
    if 'test_id' not in request.session:
        return redirect('user_login')
    try:
        test = Tests.objects.get(test_id=request.session['test_id'])
        user = Users.objects.get(user_id=request.session['user_id'])
        current_time = timezone.now()

        # # Save current
        # current_index = request.session.get('current_index', 0)
        # question_ids = request.session.get('question_ids', [])
        # if current_index < len(question_ids):
        #     try:
        #         q = Question.objects.get(question_id=question_ids[current_index])
        #         qa = TestUserQuestionAnswer.objects.get(user=user, test=test, question=q)
        #         user_answer = request.session.get('answers', {}).get(str(current_index), '')
        #         mark_review = request.session.get('marked_for_review', {}).get(str(current_index), False)
        #         qa.user_answer = user_answer
        #         qa.actual_answer = q.correct_answer
        #         qa.is_correct = user_answer == q.correct_answer if user_answer else None
        #         qa.score = 1 if user_answer == q.correct_answer else 0
        #         qa.status = 'review' if mark_review else ('answered' if user_answer else 'not_answered')
        #         qa.submitted_at = current_time
        #         if not qa.start_time:
        #             qa.start_time = current_time
        #         qa.end_time = current_time
        #         qa.save()
        #     except Exception:
        #         pass

        question_ids = request.session['question_ids']
        if request.method == 'POST':
            current_index = int(request.POST.get('question_index', 0))
            user_answer = request.POST.get('answer', '')
            mark_review = 'mark_review' in request.POST
            request.session['answers'][str(current_index)] = user_answer
            request.session['marked_for_review'][str(current_index)] = mark_review
            request.session.modified = True
            status = 'review' if mark_review else ('answered' if user_answer else 'not_answered')

            question = Question.objects.get(question_id=question_ids[current_index])
            question_answer, created = TestUserQuestionAnswer.objects.get_or_create(
                user=user, test=test, question=question,
                # defaults={'start_time': timezone.now(), 'option_order': 'A,B,C,D'}
                defaults={'start_time': timezone.now()}
            )
            
            question_answer.user_answer = user_answer
            question_answer.actual_answer = question.correct_answer
            question_answer.is_correct = user_answer == question.correct_answer if user_answer else None
            question_answer.score = 1 if user_answer == question.correct_answer else 0
            question_answer.status = status
            question_answer.submitted_at = timezone.now()
            question_answer.end_time = timezone.now()
            question_answer.save()

        test.is_active = False
        test.is_submitted = True
        test.submission_time = current_time
        test.test_status = 2
        test.suspicious_activity_count = int(request.POST.get('suspicious_activity_count', test.suspicious_activity_count))
        test.save()

        answers = TestUserQuestionAnswer.objects.filter(test=test)
        total_questions = get_config_value('gt_total_questions', 30, int)
        total_attempted = answers.exclude(user_answer='').count()
        total_correct = answers.filter(is_correct=True).count()
        percentage = (total_correct / total_questions * 100) if total_questions else 0
        cutoff = get_config_value('gt_cutoff_pass_score', 15, int)
        result_status = 'pass' if total_correct >= cutoff else 'fail'
        Result.objects.update_or_create(
            test=test, user=user,
            defaults=dict(
                total_questions=total_questions,
                total_attempted_questions=total_attempted,
                total_correct_answers=total_correct,
                percentage=percentage,
                cutoff_pass_score=cutoff,
                result_status=result_status
            )
        )
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error submitting test: {e}'})

    # clear session
    for k in ['test_id', 'question_ids', 'current_index', 'answers',
              'marked_for_review', 'start_time', 'remaining_seconds', 'original_start_time']:
        request.session.pop(k, None)
    request.session.modified = True

    messages.success(request, 'General Test submitted successfully!')
    if request.POST.get('action') == 'submit_and_logout':
        return redirect('user_logout')
    return redirect('test_selection')

@login_required
def select_language(request):
    try:
        user = Users.objects.get(user_id=request.session['user_id'])
    except Users.DoesNotExist:
        return redirect('user_login')

    if Tests.objects.filter(user=user,test_type='TT').exists():
        return redirect('test_selection')

    # clear session
    for k in ['test_id', 'question_ids', 'current_index', 'answers',
              'marked_for_review', 'start_time', 'selected_language']:
        request.session.pop(k, None)

    try:
        config_key = get_config_key_with_year('programming_languages')
        languages = Configuration.objects.filter(key=config_key, deleted=False).values_list('value', flat=True)
        if not languages:
            return render(request, 'error.html', {'message': 'No programming languages configured.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving languages: {e}'})

    if request.method == 'POST':
        selected_language = request.POST.get('language', '')
        if selected_language not in languages:
            return render(request, 'error.html', {'message': 'Invalid language selected.'})
        request.session['selected_language'] = selected_language
        request.session.modified = True
        return redirect('start_technical_test')

    return render(request, 'select_language.html', {'languages': languages})


@login_required
def start_technical_test(request):
    try:
        user = Users.objects.get(user_id=request.session['user_id'])
    except Users.DoesNotExist:
        return redirect('user_login')

    selected_language = request.session.get('selected_language')
    if not selected_language:
        return redirect('select_language')

    # prevent retake
    if Tests.objects.filter(user=user, test_type='TT', is_submitted=True, test_name__icontains=selected_language).exists():
        messages.info(request, f'You have already completed the Technical Test for {selected_language}.')
        return redirect('test_selection')

    # resume active
    try:
        active_tests = Tests.objects.filter(
            user=user, is_submitted=False, test_type='TT', test_name__icontains=selected_language
        ).order_by('-start_time')
        if active_tests.exists():
            existing_test = active_tests[0]
            current_time = timezone.now()
            duration_seconds = existing_test.duration_minutes * 60
            time_spent = (existing_test.submission_time or current_time) - existing_test.start_time
            remaining_seconds = max(0, duration_seconds - time_spent.total_seconds())

            if remaining_seconds <= 0:
                existing_test.is_active = False
                existing_test.is_submitted = True
                existing_test.submission_time = current_time
                existing_test.test_status = 2
                existing_test.save()

                answers = TestUserQuestionAnswer.objects.filter(test=existing_test)
                total_questions = get_config_value('tt_total_questions', 10, int)
                total_correct = answers.filter(is_correct=True).count()
                total_attempted = answers.exclude(user_answer='').count()
                percentage = (total_correct / total_questions * 100) if total_questions else 0
                cutoff = get_config_value('tt_cutoff_pass_score', 5, int)
                result_status = 'pass' if total_correct >= cutoff else 'fail'
                Result.objects.update_or_create(
                    test=existing_test, user=user,
                    defaults=dict(
                        total_questions=total_questions,
                        total_attempted_questions=total_attempted,
                        total_correct_answers=total_correct,
                        percentage=percentage,
                        cutoff_pass_score=cutoff,
                        result_status=result_status,
                        skill=selected_language
                    )
                )
                messages.info(request, 'Previous technical test expired and was auto-submitted.')
                return redirect('test_selection')

            existing_test.test_status = 1
            existing_test.save()
            question_answers = TestUserQuestionAnswer.objects.filter(test=existing_test).order_by('attempt_id')
            request.session.update({
                'test_id': existing_test.test_id,
                'question_ids': [qa.question.question_id for qa in question_answers],
                'current_index': max(0, min(request.session.get('current_index', 0), len(question_answers) - 1)),
                'answers': {str(i): qa.user_answer for i, qa in enumerate(question_answers) if qa.user_answer},
                'marked_for_review': {str(i): qa.status == 'review' for i, qa in enumerate(question_answers)},
                'start_time': current_time.timestamp(),
                'remaining_seconds': remaining_seconds,
                'original_start_time': existing_test.start_time.timestamp()
            })
            request.session.modified = True
            return redirect('technical_test_page', question_index=request.session['current_index'])
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error resuming technical test: {e}'})

    # start new
    for k in ['test_id', 'question_ids', 'current_index', 'answers',
              'marked_for_review', 'start_time', 'remaining_seconds', 'original_start_time']:
        request.session.pop(k, None)

    try:
        # config counts
        easy_coding_count = get_config_value('tt_coding_easy_questions', 2, int)
        medium_coding_count = get_config_value('tt_coding_medium_questions', 1, int)
        hard_coding_count = get_config_value('tt_coding_hard_questions', 1, int)
        easy_mcq_count = get_config_value('tt_mcq_easy_questions', 2, int)
        medium_mcq_count = get_config_value('tt_mcq_medium_questions', 2, int)
        hard_mcq_count = get_config_value('tt_mcq_hard_questions', 2, int)

        # fetch
        easy_coding_qs = list(Question.objects.filter(test_type='TT', difficulty='easy',
                                                      specialisation_name=selected_language,
                                                      is_multichoice=False, is_active=True, deleted=False))
        medium_coding_qs = list(Question.objects.filter(test_type='TT', difficulty='medium',
                                                        specialisation_name=selected_language,
                                                        is_multichoice=False, is_active=True, deleted=False))
        hard_coding_qs = list(Question.objects.filter(test_type='TT', difficulty='hard',
                                                      specialisation_name=selected_language,
                                                      is_multichoice=False, is_active=True, deleted=False))
        easy_mcq_qs = list(Question.objects.filter(test_type='TT', difficulty='easy',
                                                   specialisation_name=selected_language,
                                                   is_multichoice=True, is_active=True, deleted=False))
        medium_mcq_qs = list(Question.objects.filter(test_type='TT', difficulty='medium',
                                                     specialisation_name=selected_language,
                                                     is_multichoice=True, is_active=True, deleted=False))
        hard_mcq_qs = list(Question.objects.filter(test_type='TT', difficulty='hard',
                                                   specialisation_name=selected_language,
                                                   is_multichoice=True, is_active=True, deleted=False))

        if (len(easy_coding_qs) < easy_coding_count or
            len(medium_coding_qs) < medium_coding_count or
            len(hard_coding_qs) < hard_coding_count or
            len(easy_mcq_qs) < easy_mcq_count or
            len(medium_mcq_qs) < medium_mcq_count or
            len(hard_mcq_qs) < hard_mcq_count):
            return render(request, 'error.html', {'message': f'Not enough questions for {selected_language}.'})

        selected_questions = (
            random.sample(easy_coding_qs, easy_coding_count) +
            random.sample(medium_coding_qs, medium_coding_count) +
            random.sample(hard_coding_qs, hard_coding_count) +
            random.sample(easy_mcq_qs, easy_mcq_count) +
            random.sample(medium_mcq_qs, medium_mcq_count) +
            random.sample(hard_mcq_qs, hard_mcq_count)
        )
        random.shuffle(selected_questions)

        duration = get_config_value(f'tt_duration_minutes_{timezone.now().year}', 30, int)
        test = Tests.objects.create(
            user=user, test_name=f"Technical Test - {selected_language}", test_type='TT',
            duration_minutes=duration, start_time=timezone.now(),
            end_time=timezone.now() + timedelta(minutes=duration),
            is_active=True, is_submitted=False, suspicious_activity_count=0, test_status=1
        )

        for q in selected_questions:
            TestUserQuestionAnswer.objects.create(
                user=user, test=test, question=q, user_answer='',
                actual_answer=q.correct_answer if q.is_multichoice else q.technical_question_answer,
                is_correct=None, score=0, status='not_answered',
                submitted_at=None, end_time=None,
                option_order='A,B,C,D' if q.is_multichoice else ''
            )

        request.session.update({
            'test_id': test.test_id,
            'question_ids': [q.question_id for q in selected_questions],
            'current_index': 0,
            'answers': {},
            'marked_for_review': {},
            'start_time': test.start_time.timestamp(),
            'remaining_seconds': duration * 60,
            'original_start_time': test.start_time.timestamp()
        })
        request.session.modified = True
        return redirect('technical_test_page', question_index=0)
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error creating technical test: {e}'})


@login_required
def technical_test_page(request, question_index):
    ua = request.user_agent
    if ua.is_mobile or ua.is_tablet:
        return HttpResponseForbidden("Exams can only be taken on a Desktop device.")
    if ua.browser.family not in ["Chrome", "Firefox", "Edge"]:
        return HttpResponseForbidden("Please use Chrome, Firefox, or Edge on Desktop.")

    if 'test_id' not in request.session or 'question_ids' not in request.session or 'selected_language' not in request.session:
        return redirect('select_language')

    try:
        user = Users.objects.get(user_id=request.session['user_id'])
        test = Tests.objects.get(test_id=request.session['test_id'])
    except Tests.DoesNotExist:
        return render(request, 'error.html', {'message': 'Test not found.'})

    question_ids = request.session['question_ids']
    current_index = int(question_index)

    if current_index < request.session.get('current_index', 0):
        return redirect('technical_test_page', question_index=request.session['current_index'])

    if current_index < 0 or current_index >= len(question_ids):
        return redirect('submit_technical_test')

    try:
        question = Question.objects.get(question_id=question_ids[current_index])
        question_answer, created = TestUserQuestionAnswer.objects.get_or_create(
            user=user, test=test, question=question,
            # defaults={'start_time': timezone.now(), 'option_order': 'A,B,C,D'}
            defaults={'start_time': timezone.now()}
        )
        if not created and not question_answer.start_time:
            question_answer.start_time = timezone.now()
            question_answer.save()
    except Question.DoesNotExist:
        return render(request, 'error.html', {'message': 'Question not found.'})

    instructions = Instruction.objects.filter(test_type='TT', is_active=True).order_by('display_order')

    # Timer
    remaining_seconds = request.session.get('remaining_seconds', test.duration_minutes * 60)
    current_time = timezone.now().timestamp()
    elapsed = current_time - request.session['start_time']
    remaining_seconds = max(0, remaining_seconds - elapsed)
    request.session.update({'remaining_seconds': remaining_seconds, 'start_time': current_time,
                            'current_index': current_index})
    request.session.modified = True
    if remaining_seconds <= 0:
        return redirect('submit_technical_test')

    if request.method == 'POST':
        user_answer = request.POST.get('answer', '')
        mark_review = request.POST.get('mark_review') == 'on'
        request.session['answers'][str(current_index)] = user_answer
        if mark_review:
            request.session['marked_for_review'][str(current_index)] = True
        else:
            request.session['marked_for_review'].pop(str(current_index), None)
        request.session.modified = True

        actual_answer = question.correct_answer if question.is_multichoice else question.technical_question_answer
        status = 'review' if mark_review else ('answered' if user_answer else 'not_answered')

        question_answer.user_answer = user_answer
        question_answer.actual_answer = actual_answer
        question_answer.is_correct = user_answer == actual_answer if user_answer else None
        question_answer.score = 1 if user_answer == actual_answer else 0
        question_answer.status = status
        question_answer.submitted_at = timezone.now()
        question_answer.end_time = timezone.now()
        question_answer.save()

        if current_index > 0 and request.POST.get('action') == 'next':
            try:
                prev_q = Question.objects.get(question_id=question_ids[current_index - 1])
                prev_ans = TestUserQuestionAnswer.objects.get(user=user, test=test, question=prev_q)
                if not prev_ans.end_time:
                    prev_ans.end_time = timezone.now()
                    prev_ans.save()
            except Exception:
                pass

        test.is_active = True
        test.save()

        action = request.POST.get('action')
        if action == 'next':
            if current_index + 1 < len(question_ids):
                return redirect('technical_test_page', question_index=current_index + 1)
            else:
                return redirect('submit_technical_test')

        elif action == 'prev' and current_index > 0:
            return redirect('technical_test_page', question_index=current_index - 1)
        elif action == 'submit':
            return redirect('submit_technical_test')

    answers = request.session.get('answers', {})
    marked_for_review = request.session.get('marked_for_review', {})
    context = {
        'question': question,
        'current_index': current_index,
        'total_questions': len(question_ids),
        'remaining_time': remaining_seconds,
        'answers': answers,
        'marked_for_review': marked_for_review,
        'question_range': range(len(question_ids)),
        'saved_answer': answers.get(str(current_index), ''),
        'saved_review': marked_for_review.get(str(current_index), False),
        'selected_language': request.session.get('selected_language'),
        'user': user,
        'options': ['A', 'B', 'C', 'D'],  # fixed order
        'instructions': instructions,
        'test': test,
        'alert_duration': get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
        'alert_cooldown': get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
    }
    return render(request, 'technical_test_page.html', context)

@login_required
def submit_technical_test(request):
    if 'test_id' not in request.session:
        return redirect('select_language')

    try:
        test = Tests.objects.get(test_id=request.session['test_id'])
        user = Users.objects.get(user_id=request.session['user_id'])
        current_time = timezone.now()

        # # Save current
        # current_index = request.session.get('current_index', 0)
        # question_ids = request.session.get('question_ids', [])
        # if current_index < len(question_ids):
        #     try:
        #         q = Question.objects.get(question_id=question_ids[current_index])
        #         qa = TestUserQuestionAnswer.objects.get(user=user, test=test, question=q)
        #         user_answer = request.session.get('answers', {}).get(str(current_index), '')
        #         mark_review = request.session.get('marked_for_review', {}).get(str(current_index), False)
        #         actual_answer = q.correct_answer if q.is_multichoice else q.technical_question_answer
        #         qa.user_answer = user_answer
        #         qa.actual_answer = actual_answer
        #         qa.is_correct = user_answer == actual_answer if user_answer else None
        #         qa.score = 1 if user_answer == actual_answer else 0
        #         qa.status = 'review' if mark_review else ('answered' if user_answer else 'not_answered')
        #         qa.submitted_at = current_time
        #         if not qa.start_time:
        #             qa.start_time = current_time
        #         qa.end_time = current_time
        #         qa.save()
        #     except Exception:
        #         pass
        if request.method == 'POST':
            current_index = request.session.get('current_index', 0)
            user_answer = request.POST.get('answer', '')
            mark_review = request.POST.get('mark_review') == 'on'
            request.session['answers'][str(current_index)] = user_answer
            if mark_review:
                request.session['marked_for_review'][str(current_index)] = True
            else:
                request.session['marked_for_review'].pop(str(current_index), None)
            request.session.modified = True

            question_ids = request.session.get('question_ids', [])
            question = Question.objects.get(question_id=question_ids[current_index])
            question_answer, created = TestUserQuestionAnswer.objects.get_or_create(
                user=user, test=test, question=question
            )

            actual_answer = question.correct_answer if question.is_multichoice else question.technical_question_answer
            status = 'review' if mark_review else ('answered' if user_answer else 'not_answered')

            question_answer.user_answer = user_answer
            question_answer.actual_answer = actual_answer
            question_answer.is_correct = user_answer == actual_answer if user_answer else None
            question_answer.score = 1 if user_answer == actual_answer else 0
            question_answer.status = status
            question_answer.submitted_at = timezone.now()
            question_answer.end_time = timezone.now()
            question_answer.save()

        test.is_active = False
        test.is_submitted = True
        test.submission_time = current_time
        test.test_status = 2
        test.suspicious_activity_count = int(request.POST.get('suspicious_activity_count', test.suspicious_activity_count))
        test.save()

        # calculate result
        answers = TestUserQuestionAnswer.objects.filter(test=test)
        total_questions = get_config_value('tt_total_questions', 10, int)
        total_attempted = answers.exclude(user_answer='').count()
        total_correct = answers.filter(is_correct=True).count()
        percentage = (total_correct / total_questions * 100) if total_questions else 0
        cutoff = get_config_value('tt_cutoff_pass_score', 5, int)
        result_status = 'pass' if total_correct >= cutoff else 'fail'
        Result.objects.update_or_create(
            test=test, user=user,
            defaults=dict(
                total_questions=total_questions,
                total_attempted_questions=total_attempted,
                total_correct_answers=total_correct,
                percentage=percentage,
                cutoff_pass_score=cutoff,
                skill=request.session.get('selected_language'),
                result_status=result_status
            )
        )

        # send confirmation email
        subject = "Submission Confirmation"
        to_email = [user.email]
        context = {
            'first_name': user.first_name,
            'test_name': test.test_name,
            'total_questions': total_questions,
            'total_attempted': total_attempted,
            'total_correct': total_correct,
            'percentage': percentage,
            'result_status': 'Pass' if total_correct >= cutoff else 'Fail'
        }
        html_message = render_to_string('emails/technical_test_submitted.html', context)
        send_mail(
            subject, '', settings.DEFAULT_FROM_EMAIL, to_email,
            html_message=html_message, fail_silently=True
        )
        user.submission_mail_sent = True
        user.save()
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error submitting technical test: {e}'})

    # clear session
    for k in ['test_id', 'question_ids', 'current_index', 'answers', 'marked_for_review',
              'start_time', 'remaining_seconds', 'original_start_time', 'selected_language']:
        request.session.pop(k, None)
    request.session.modified = True

    messages.success(request, 'Technical Test submitted successfully!')
    if request.POST.get('action') == 'submit_and_logout':
        return redirect('user_logout')
    return redirect('test_selection')


# ------------------------ Resolution Mismatch ------------------------

@csrf_exempt
def update_resolution_mismatch(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    test_id = request.session.get('test_id')
    try:
        test = Tests.objects.get(test_id=test_id, user__user_id=request.session.get('user_id'))
        test.resolution_mismatch_count += 1
        test.save()
        return JsonResponse({
            'status': 'success',
            'resolution_mismatch_count': test.resolution_mismatch_count,
            'auto_submit': test.resolution_mismatch_count >= 3
        })
    except Tests.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Test not found'}, status=404)


# ------------------------ Screenshot Capture ------------------------

@csrf_exempt
def update_test_location(request):
    if request.method == "POST":
        try:
            test_id = request.session.get("test_id")
            lat = request.POST.get("latitude")
            lng = request.POST.get("longitude")

            if not test_id or not lat or not lng:
                return JsonResponse({"status": "error", "message": "Missing parameters"}, status=400)

            test = Tests.objects.get(test_id=test_id, user__user_id=request.session.get("user_id"))
            test.location_lat = lat
            test.location_lng = lng
            test.save()

            return JsonResponse({"status": "success"})
        except Tests.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Test not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_exempt
def captureScreenshot(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

    try:
        user_id = request.session.get('user_id')
        photo_type = request.POST.get('photo_type')
        image_data = request.POST.get('image')

        if not user_id or not photo_type or not image_data:
            return JsonResponse({'success': False, 'error': 'Missing required parameters'}, status=400)
        if photo_type not in ['GT', 'TT', 'INST']:
            return JsonResponse({'success': False, 'error': 'Invalid photo type'}, status=400)

        user = Users.objects.get(user_id=user_id)

        # verify active test for GT/TT
        if photo_type in ['GT', 'TT']:
            test_id = request.session.get('test_id')
            if not test_id:
                return JsonResponse({'success': False, 'error': 'No active test found'}, status=400)
            Tests.objects.get(test_id=test_id, user=user)

        # decode base64
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        if ext not in ['jpeg', 'jpg', 'png']:
            ext = 'jpg'
        data = base64.b64decode(imgstr)

        # generate file path
        field_name = {'GT': 'gt_images', 'TT': 'tt_images', 'INST': 'inst_images'}[photo_type]
        current_images = getattr(user, field_name) or []
        sequence = len(current_images) + 1
        registration_id = user.registration_id
        file_name = f"{registration_id}_verifiedexam_{photo_type}_{sequence}.{ext}"
        file_path = os.path.join('media', registration_id, 'Exam_images', file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # save
        with open(file_path, 'wb') as f:
            f.write(data)

        # update user
        current_images.append(file_path)
        setattr(user, field_name, current_images)
        user.save()

        return JsonResponse({'success': True, 'message': 'Screenshot captured successfully'})
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    except Tests.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Test not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
def log_browser(request):
    if request.method == 'POST':
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        browser = 'Unknown Browser'

        if 'Firefox' in user_agent:
            browser = 'Mozilla Firefox'
        elif 'Edg' in user_agent:
            browser = 'Microsoft Edge'
        elif 'Chrome' in user_agent:
            browser = 'Google Chrome'
        elif 'Safari' in user_agent:
            browser = 'Apple Safari'

        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

        try:
            user = Users.objects.get(user_id=user_id)
        except Users.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

        test = Tests.objects.filter(user=user, is_submitted=False).order_by('-created_at').first()
        if test:
            test.browser_used = browser
            test.save()
            return JsonResponse({'status': 'success', 'browser': browser})
        else:
            return JsonResponse({'status': 'error', 'message': 'No active test found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)