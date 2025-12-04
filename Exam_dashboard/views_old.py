from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib import messages
from home.users.models import Tests, TestUserQuestionAnswer, Users, Result, Question, Configuration, Instruction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import timedelta, datetime
from functools import wraps
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import base64
import os

current_year = datetime.now().year

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('user_login')
        return view_func(request, *args, **kwargs)
    return wrapper

def get_config_key_with_year(key):
    current_year = datetime.now().year
    return f"{key}_{current_year}"

def get_config_value(key, default=None, cast_type=None):
    try:
        config_key = get_config_key_with_year(key)
        config = Configuration.objects.get(key=config_key, deleted=False)
        value = config.value
        if cast_type:
            return cast_type(value)
        return value
    except Configuration.DoesNotExist:
        try:
            config = Configuration.objects.get(key=key, deleted=False)
            value = config.value
            if cast_type:
                return cast_type(value)
            return value
        except Configuration.DoesNotExist:
            return default
    except Exception as e:
        return default

@csrf_exempt
def update_suspicious_activity(request):
    if request.method == 'POST':
        test_id = request.session.get('test_id')
        person_count = int(request.POST.get('person_count', 0))
        try:
            test = Tests.objects.get(test_id=test_id, user__user_id=request.session.get('user_id'))
            freeze_popup = False
            auto_submit = False

            if person_count == 0 or person_count > 1:
                test.suspicious_activity_count += 1
                test.save()
                
                # Fetch max counts from config
                freeze_threshold = get_config_value('suspicious_activity_majorpopup', 3, int)
                max_freeze_count = get_config_value('suspicious_activity_count', 9, int)

                # Freeze popup logic
                if test.suspicious_activity_count % freeze_threshold == 0 and test.suspicious_activity_count < max_freeze_count:
                    freeze_popup = True

                # Auto submit logic
                auto_submit_threshold = get_config_value('suspicious_activity_count', 9, int)
                if test.suspicious_activity_count >= auto_submit_threshold:
                    auto_submit = True

            response_data = {
                'status': 'success',
                'suspicious_activity_count': test.suspicious_activity_count,
                'freeze_popup': freeze_popup,
                'auto_submit': auto_submit,
                'freeze_timer': get_config_value('freeze_Major_popup_timesec', 50, int)  # send timer value dynamically
            }
            return JsonResponse(response_data)

        except Tests.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Test not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



@login_required
def start_test(request):
    try:
        user = Users.objects.get(user_id=request.session['user_id'])
    except Users.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found. Please log in again.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving user: {str(e)}'})

    # Only allow starting a new test if user does NOT have any submitted test of type GT
    submitted_tests = Tests.objects.filter(user=user, test_type='GT', is_submitted=True)
    if submitted_tests.exists():
        messages.info(request, 'You have already completed and submitted the General Test.')
        return redirect('test_selection')

    try:
        active_tests = Tests.objects.filter(user=user, is_submitted=False, test_type='GT').order_by('-start_time')
        if active_tests.exists():
            existing_test = active_tests[0]
            current_time = timezone.now()
            duration_seconds = existing_test.duration_minutes * 60
            if existing_test.submission_time:
                time_spent_seconds = (existing_test.submission_time - existing_test.start_time).total_seconds()
            else:
                time_spent_seconds = (current_time - existing_test.start_time).total_seconds()
            remaining_seconds = max(0, duration_seconds - time_spent_seconds)

            if remaining_seconds <= 0:
                existing_test.is_active = False
                existing_test.is_submitted = True
                existing_test.submission_time = current_time
                existing_test.test_status = 2  # Set test_status to 2 on auto-submission
                existing_test.save()
                answers = TestUserQuestionAnswer.objects.filter(test=existing_test)
                total_questions = get_config_value('gt_total_questions', 30, int)
                total_attempted = answers.exclude(user_answer='').count()
                total_correct = answers.filter(is_correct=True).count()
                percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
                cutoff_pass_score = get_config_value('gt_cutoff_pass_score', 15, int)
                result_status = 'pass' if total_correct >= cutoff_pass_score else 'fail'
                Result.objects.update_or_create(
                    test=existing_test,
                    user=user,
                    defaults={
                        'total_questions': total_questions,
                        'total_attempted_questions': total_attempted,
                        'total_correct_answers': total_correct,
                        'percentage': percentage,
                        'cutoff_pass_score': cutoff_pass_score,
                        'result_status': result_status
                    }
                )
                messages.info(request, 'Previous test duration expired and was auto-submitted.')
                return redirect('test_selection')

            existing_test.test_status = 1  # Ensure test_status is 1 for resumed test
            existing_test.save()
            request.session['test_id'] = existing_test.test_id
            question_answers = TestUserQuestionAnswer.objects.filter(test=existing_test).order_by('attempt_id')
            question_ids = [qa.question.question_id for qa in question_answers]
            if not question_ids:
                return render(request, 'error.html', {'message': 'No questions found for the existing test.'})
            request.session['question_ids'] = question_ids
            request.session['current_index'] = request.session.get('current_index', 0)
            if request.session['current_index'] < 0 or request.session['current_index'] >= len(question_ids):
                request.session['current_index'] = 0
            answers = {str(i): qa.user_answer for i, qa in enumerate(question_answers) if qa.user_answer}
            marked_for_review = {str(i): qa.status == 'review' for i, qa in enumerate(question_answers)}
            request.session['answers'] = answers
            request.session['marked_for_review'] = marked_for_review
            request.session['start_time'] = current_time.timestamp()
            request.session['remaining_seconds'] = remaining_seconds
            request.session['original_start_time'] = existing_test.start_time.timestamp()
            request.session.modified = True
            return redirect('test_page', question_index=request.session['current_index'])
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving existing test: {str(e)}'})

    keys_to_clear = ['test_id', 'question_ids', 'current_index', 'answers', 'marked_for_review', 'start_time', 'remaining_seconds', 'original_start_time']
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]

    try:
        easy_questions = list(Question.objects.filter(test_type='GT', difficulty='easy', is_active=True))
        medium_questions = list(Question.objects.filter(test_type='GT', difficulty='medium', is_active=True))
        hard_questions = list(Question.objects.filter(test_type='GT', difficulty='hard', is_active=True))
        easy_count = get_config_value('gt_easy_questions', 10, int)
        medium_count = get_config_value('gt_medium_questions', 10, int)
        hard_count = get_config_value('gt_hard_questions', 10, int)
        if len(easy_questions) < easy_count or len(medium_questions) < medium_count or len(hard_questions) < hard_count:
            return render(request, 'error.html', {'message': 'Not enough questions available to start the test.'})
        selected_easy = random.sample(easy_questions, easy_count)
        selected_medium = random.sample(medium_questions, medium_count)
        selected_hard = random.sample(hard_questions, hard_count)
        selected_questions = selected_easy + selected_medium + selected_hard
        random.shuffle(selected_questions)
        duration_minutes = get_config_value('gt_duration_minutes', 30, int)
        test = Tests.objects.create(
            user=user,
            test_name="General Test",
            test_type='GT',
            duration_minutes=duration_minutes,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(minutes=duration_minutes),
            is_active=True,
            is_submitted=False,
            suspicious_activity_count=0,
            test_status=1  # Set test_status to 1 when starting a new test
        )
        for question in selected_questions:
            options = ['A', 'B', 'C', 'D']
            shuffled_options = random.sample(options, len(options))
            option_order = ','.join(shuffled_options)
            TestUserQuestionAnswer.objects.create(
                user=user,
                test=test,
                question=question,
                user_answer='',
                actual_answer=question.correct_answer,
                is_correct=None,
                score=0,
                status='not_answered',
                submitted_at=None,
                end_time=None,
                option_order=option_order
            )
        request.session['test_id'] = test.test_id
        request.session['question_ids'] = [q.question_id for q in selected_questions]
        request.session['current_index'] = 0
        request.session['answers'] = {}
        request.session['marked_for_review'] = {}
        request.session['start_time'] = test.start_time.timestamp()
        request.session['remaining_seconds'] = duration_minutes * 60
        request.session['original_start_time'] = test.start_time.timestamp()
        request.session.modified = True
        request.session.save()
        return redirect('test_page', question_index=0)
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error creating new test: {str(e)}'})

from django.views.decorators.csrf import csrf_exempt

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

@login_required
def test_page(request, question_index):
    # Device restriction (server-side)
    ua = request.user_agent
    if ua.is_mobile or ua.is_tablet:
        return HttpResponseForbidden("Exams can only be taken on a Desktop device.")
    allowed_browsers = ["Chrome", "Firefox", "Edge"]
    if ua.browser.family not in allowed_browsers:
        return HttpResponseForbidden("Please use Chrome, Firefox, or Edge on Desktop.")

    try:
        user = Users.objects.get(user_id=request.session['user_id'])
    except Users.DoesNotExist:
        return redirect('user_login')
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving user: {str(e)}'})
    
    if 'test_id' not in request.session or 'question_ids' not in request.session:
        return redirect('start_test')
    
    try:
        test = Tests.objects.get(test_id=request.session['test_id'])
    except Tests.DoesNotExist:
        return render(request, 'error.html', {'message': 'Test not found.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving test: {str(e)}'})
    
    test_id = request.session['test_id']
    question_ids = request.session['question_ids']
    current_index = int(question_index)
    # Prevent navigation to previous questions
    session_current_index = request.session.get('current_index', 0)
    if current_index < session_current_index:
        return redirect('test_page', question_index=session_current_index)
    
    if current_index < 0 or current_index >= len(question_ids):
        return redirect('submit_test')
    
    try:
        question = Question.objects.get(question_id=question_ids[current_index])
        question_answer, created = TestUserQuestionAnswer.objects.get_or_create(
            user=user,
            test=test,
            question=question,
            defaults={
                'start_time': timezone.now(),
                'option_order': ','.join(['A', 'B', 'C', 'D'])  # Default option order
            }
        )
        # Update start_time if the record already exists
        if not created and not question_answer.start_time:
            question_answer.start_time = timezone.now()
            question_answer.save()
    except Question.DoesNotExist:
        return render(request, 'error.html', {'message': 'Question not found.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving question: {str(e)}'})
    
    # Fetch instructions for General Test
    try:
        instructions = Instruction.objects.filter(test_type='GT', is_active=True).order_by('display_order')
    except Exception as e:
        instructions = []
    
    remaining_seconds = request.session.get('remaining_seconds', test.duration_minutes * 60)
    current_time = timezone.now().timestamp()
    elapsed_time = current_time - request.session['start_time']
    remaining_seconds = max(0, remaining_seconds - elapsed_time)
    request.session['remaining_seconds'] = remaining_seconds
    request.session['start_time'] = current_time
    request.session['current_index'] = current_index  # Update current_index in session
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
        
        # Update current question's answer and timestamps
        question_answer.user_answer = user_answer
        question_answer.actual_answer = question.correct_answer
        question_answer.is_correct = user_answer == question.correct_answer if user_answer else None
        question_answer.score = 1 if user_answer == question.correct_answer else 0
        question_answer.status = status
        question_answer.submitted_at = timezone.now()
        question_answer.end_time = timezone.now()
        question_answer.save()
        
        # Update previous question's end_time if applicable
        if current_index > 0 and request.POST.get('action') == 'next':
            try:
                prev_question = Question.objects.get(question_id=question_ids[current_index - 1])
                prev_question_answer = TestUserQuestionAnswer.objects.get(
                    user=user, test=test, question=prev_question
                )
                if not prev_question_answer.end_time:
                    prev_question_answer.end_time = timezone.now()
                    prev_question_answer.save()
            except (Question.DoesNotExist, TestUserQuestionAnswer.DoesNotExist):
                pass  # Skip if previous question or answer record doesn't exist
        
        test.is_active = True
        test.save()
        
        action = request.POST.get('action')
        if action == 'next':
            next_index = current_index + 1
            if next_index < len(question_ids):
                return redirect('test_page', question_index=next_index)
            else:
                return redirect('submit_test')
        elif action == 'prev':
            prev_index = current_index - 1
            if prev_index >= 0:
                return redirect('test_page', question_index=prev_index)
        elif action == 'submit':
            return redirect('submit_test')
    
    answers = request.session.get('answers', {})
    marked_for_review = request.session.get('marked_for_review', {})
    saved_answer = answers.get(str(current_index), '')
    saved_review = marked_for_review.get(str(current_index), False)
    shuffled_options = question_answer.get_shuffled_options()
    context = {
        'question': question,
        'current_index': current_index,
        'total_questions': len(question_ids),
        'remaining_time': remaining_seconds,
        'answers': answers,
        'marked_for_review': marked_for_review,
        'question_range': range(len(question_ids)),
        'saved_answer': saved_answer,
        'saved_review': saved_review,
        'user': user,
        'shuffled_options': shuffled_options,
        'instructions': instructions,
        'test': test,
        'alert_duration' : get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
        'alert_cooldown' : get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
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
        # Update the current question's answer and timestamps
        current_index = request.session.get('current_index', 0)
        question_ids = request.session.get('question_ids', [])
        if current_index < len(question_ids):
            try:
                question = Question.objects.get(question_id=question_ids[current_index])
                question_answer = TestUserQuestionAnswer.objects.get(
                    user=user, test=test, question=question
                )
                user_answer = request.session.get('answers', {}).get(str(current_index), '')
                mark_review = request.session.get('marked_for_review', {}).get(str(current_index), False)
                status = 'review' if mark_review else ('answered' if user_answer else 'not_answered')
                
                question_answer.user_answer = user_answer
                question_answer.actual_answer = question.correct_answer
                question_answer.is_correct = user_answer == question.correct_answer if user_answer else None
                question_answer.score = 1 if user_answer == question.correct_answer else 0
                question_answer.status = status
                question_answer.submitted_at = current_time
                if not question_answer.start_time:  # Set start_time if not already set
                    question_answer.start_time = current_time
                question_answer.end_time = current_time
                question_answer.save()
            except (Question.DoesNotExist, TestUserQuestionAnswer.DoesNotExist):
                pass  # Skip if question or answer record doesn't exist
        test.is_active = False
        test.is_submitted = True
        test.submission_time = current_time
        test.test_status = 2  # Set test_status to 2 on submission
        suspicious_count = int(request.POST.get('suspicious_activity_count', test.suspicious_activity_count))
        test.suspicious_activity_count = suspicious_count
        test.save()
    except Tests.DoesNotExist:
        return render(request, 'error.html', {'message': 'Test not found.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error updating test: {str(e)}'})
    
    try:
        answers = TestUserQuestionAnswer.objects.filter(test=test)
        total_questions = get_config_value('gt_total_questions', 30, int)
        total_attempted = answers.exclude(user_answer='').count()
        total_correct = answers.filter(is_correct=True).count()
        percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
        cutoff_pass_score = get_config_value('gt_cutoff_pass_score', 15, int)
        result_status = 'pass' if total_correct >= cutoff_pass_score else 'fail'
        Result.objects.update_or_create(
            test=test,
            user=test.user,
            defaults={
                'total_questions': total_questions,
                'total_attempted_questions': total_attempted,
                'total_correct_answers': total_correct,
                'percentage': percentage,
                'cutoff_pass_score': cutoff_pass_score,
                'result_status': result_status
            }
        )
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error saving test results: {str(e)}'})

    keys_to_clear = ['test_id', 'question_ids', 'current_index', 'answers', 'marked_for_review', 'start_time', 'remaining_seconds', 'original_start_time']
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]
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
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving user: {str(e)}'})
    
    keys_to_clear = ['test_id', 'question_ids', 'current_index', 'answers', 'marked_for_review', 'start_time', 'selected_language']
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]
    
    try:
        config_key = get_config_key_with_year('programming_languages')
        languages = Configuration.objects.filter(key=config_key, deleted=False).values_list('value', flat=True)
        if not languages:
            return render(request, 'error.html', {'message': 'No programming languages configured.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving languages: {str(e)}'})
    
    if request.method == 'POST':
        selected_language = request.POST.get('language', '')
        if selected_language not in languages:
            return render(request, 'error.html', {'message': 'Invalid language selected.'})
        request.session['selected_language'] = selected_language
        request.session.modified = True
        return redirect('start_technical_test')
    
    context = {
        'languages': languages,
    }
    return render(request, 'select_language.html', context)

@login_required
def start_technical_test(request):
    try:
        user = Users.objects.get(user_id=request.session['user_id'])
    except Users.DoesNotExist:
        return redirect('user_login')
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving user: {str(e)}'})

    selected_language = request.session.get('selected_language')
    if not selected_language:
        return redirect('select_language')

    # Only allow starting a new technical test if user does NOT have any submitted test of type TT for the selected language
    submitted_tests = Tests.objects.filter(
        user=user, test_type='TT', is_submitted=True, test_name__icontains=selected_language
    )
    if submitted_tests.exists():
        messages.info(request, f'You have already completed and submitted the Technical Test for {selected_language}.')
        return redirect('test_selection')

    try:
        active_tests = Tests.objects.filter(
            user=user, is_submitted=False, test_type='TT', test_name__icontains=selected_language
        ).order_by('-start_time')
        if active_tests.exists():
            existing_test = active_tests[0]
            current_time = timezone.now()
            duration_seconds = existing_test.duration_minutes * 60
            if existing_test.submission_time:
                time_spent_seconds = (existing_test.submission_time - existing_test.start_time).total_seconds()
            else:
                time_spent_seconds = (current_time - existing_test.start_time).total_seconds()
            remaining_seconds = max(0, duration_seconds - time_spent_seconds)

            if remaining_seconds <= 0:
                existing_test.is_active = False
                existing_test.is_submitted = True
                existing_test.submission_time = current_time
                existing_test.test_status = 2  # Set test_status to 2 on auto-submission
                existing_test.save()
                answers = TestUserQuestionAnswer.objects.filter(test=existing_test)
                total_questions = get_config_value('tt_total_questions', 10, int)
                total_attempted = answers.exclude(user_answer='').count()
                total_correct = answers.filter(is_correct=True).count()
                percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
                cutoff_pass_score = get_config_value('tt_cutoff_pass_score', 5, int)
                result_status = 'pass' if total_correct >= cutoff_pass_score else 'fail'
                Result.objects.update_or_create(
                    test=existing_test,
                    user=user,
                    defaults={
                        'total_questions': total_questions,
                        'total_attempted_questions': total_attempted,
                        'total_correct_answers': total_correct,
                        'percentage': percentage,
                        'cutoff_pass_score': cutoff_pass_score,
                        'result_status': result_status,
                        'skill': selected_language
                    }
                )
                messages.info(request, 'Previous technical test duration expired and was auto-submitted.')
                return redirect('test_selection')

            existing_test.test_status = 1  # Ensure test_status is 1 for resumed test
            existing_test.save()
            request.session['test_id'] = existing_test.test_id
            question_answers = TestUserQuestionAnswer.objects.filter(test=existing_test).order_by('attempt_id')
            question_ids = [qa.question.question_id for qa in question_answers]
            if not question_ids:
                return render(request, 'error.html', {'message': 'No questions found for the existing test.'})
            request.session['question_ids'] = question_ids
            request.session['current_index'] = request.session.get('current_index', 0)
            if request.session['current_index'] < 0 or request.session['current_index'] >= len(question_ids):
                request.session['current_index'] = 0
            answers = {str(i): qa.user_answer for i, qa in enumerate(question_answers) if qa.user_answer}
            marked_for_review = {str(i): qa.status == 'review' for i, qa in enumerate(question_answers)}
            request.session['answers'] = answers
            request.session['marked_for_review'] = marked_for_review
            request.session['start_time'] = current_time.timestamp()
            request.session['remaining_seconds'] = remaining_seconds
            request.session['original_start_time'] = existing_test.start_time.timestamp()
            request.session.modified = True
            return redirect('technical_test_page', question_index=request.session['current_index'])
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving existing test: {str(e)}'})

    keys_to_clear = ['test_id', 'question_ids', 'current_index', 'answers', 'marked_for_review', 'start_time', 'remaining_seconds', 'original_start_time']
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]

    try:
        easy_coding_count = get_config_value('tt_coding_easy_questions', 2, int)
        medium_coding_count = get_config_value('tt_coding_medium_questions', 1, int)
        hard_coding_count = get_config_value('tt_coding_hard_questions', 1, int)
        easy_mcq_count = get_config_value('tt_mcq_easy_questions', 2, int)
        medium_mcq_count = get_config_value('tt_mcq_medium_questions', 2, int)
        hard_mcq_count = get_config_value('tt_mcq_hard_questions', 2, int)
        total_questions = (easy_coding_count + medium_coding_count + hard_coding_count +
                           easy_mcq_count + medium_mcq_count + hard_mcq_count)

        easy_coding_questions = list(Question.objects.filter(
            test_type='TT', difficulty='easy', specialisation_name=selected_language,
            is_multichoice=False, is_active=True, deleted=False))
        medium_coding_questions = list(Question.objects.filter(
            test_type='TT', difficulty='medium', specialisation_name=selected_language,
            is_multichoice=False, is_active=True, deleted=False))
        hard_coding_questions = list(Question.objects.filter(
            test_type='TT', difficulty='hard', specialisation_name=selected_language,
            is_multichoice=False, is_active=True, deleted=False))
        easy_mcq_questions = list(Question.objects.filter(
            test_type='TT', difficulty='easy', specialisation_name=selected_language,
            is_multichoice=True, is_active=True, deleted=False))
        medium_mcq_questions = list(Question.objects.filter(
            test_type='TT', difficulty='medium', specialisation_name=selected_language,
            is_multichoice=True, is_active=True, deleted=False))
        hard_mcq_questions = list(Question.objects.filter(
            test_type='TT', difficulty='hard', specialisation_name=selected_language,
            is_multichoice=True, is_active=True, deleted=False))

        if (len(easy_coding_questions) < easy_coding_count or
                len(medium_coding_questions) < medium_coding_count or
                len(hard_coding_questions) < hard_coding_count or
                len(easy_mcq_questions) < easy_mcq_count or
                len(medium_mcq_questions) < medium_mcq_count or
                len(hard_mcq_questions) < hard_mcq_count):
            return render(request, 'error.html', {
                'message': f'Not enough questions for {selected_language}. '
                           f'Required: {easy_coding_count} easy coding, {medium_coding_count} medium coding, {hard_coding_count} hard coding, '
                           f'{easy_mcq_count} easy MCQ, {medium_mcq_count} medium MCQ, {hard_mcq_count} hard MCQ. '
                           f'Available: {len(easy_coding_questions)} easy coding, {len(medium_coding_questions)} medium coding, '
                           f'{len(hard_coding_questions)} hard coding, {len(easy_mcq_questions)} easy MCQ, '
                           f'{len(medium_mcq_questions)} medium MCQ, {len(hard_mcq_questions)} hard MCQ.'
            })

        selected_easy_coding = random.sample(easy_coding_questions, easy_coding_count)
        selected_medium_coding = random.sample(medium_coding_questions, medium_coding_count)
        selected_hard_coding = random.sample(hard_coding_questions, hard_coding_count)
        selected_easy_mcq = random.sample(easy_mcq_questions, easy_mcq_count)
        selected_medium_mcq = random.sample(medium_mcq_questions, medium_mcq_count)
        selected_hard_mcq = random.sample(hard_mcq_questions, hard_mcq_count)

        selected_questions = (selected_easy_coding + selected_medium_coding + selected_hard_coding +
                             selected_easy_mcq + selected_medium_mcq + selected_hard_mcq)
        random.shuffle(selected_questions)

        duration_minutes = get_config_value('tt_duration_minutes_' + str(timezone.now().year), 30, int)
        test = Tests.objects.create(
            user=user,
            test_name=f"Technical Test - {selected_language}",
            test_type='TT',
            duration_minutes=duration_minutes,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(minutes=duration_minutes),
            is_active=True,
            is_submitted=False,
            suspicious_activity_count=0,
            test_status=1  # Set test_status to 1 when starting a new test
        )

        for question in selected_questions:
            option_order = ''
            if question.is_multichoice:
                options = ['A', 'B', 'C', 'D']
                shuffled_options = random.sample(options, len(options))
                option_order = ','.join(shuffled_options)
            TestUserQuestionAnswer.objects.create(
                user=user,
                test=test,
                question=question,
                user_answer='',
                actual_answer=question.correct_answer if question.is_multichoice else question.technical_question_answer,
                is_correct=None,
                score=0,
                status='not_answered',
                submitted_at=None,
                end_time=None,
                option_order=option_order
            )

        request.session['test_id'] = test.test_id
        request.session['question_ids'] = [q.question_id for q in selected_questions]
        request.session['current_index'] = 0
        request.session['answers'] = {}
        request.session['marked_for_review'] = {}
        request.session['start_time'] = test.start_time.timestamp()
        request.session['remaining_seconds'] = duration_minutes * 60
        request.session['original_start_time'] = test.start_time.timestamp()
        request.session.modified = True
        request.session.save()
        return redirect('technical_test_page', question_index=0)
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error creating new test: {str(e)}'})

@login_required
def technical_test_page(request, question_index):
    # Device restriction (server-side)
    ua = request.user_agent
    if ua.is_mobile or ua.is_tablet:
        return HttpResponseForbidden("Exams can only be taken on a Desktop device.")
    allowed_browsers = ["Chrome", "Firefox", "Edge"]
    if ua.browser.family not in allowed_browsers:
        return HttpResponseForbidden("Please use Chrome, Firefox, or Edge on Desktop.")
    
    if 'test_id' not in request.session or 'question_ids' not in request.session or 'selected_language' not in request.session:
        return redirect('select_language')
    
    try:
        user = Users.objects.get(user_id=request.session['user_id'])
        test = Tests.objects.get(test_id=request.session['test_id'])
    except Tests.DoesNotExist:
        return render(request, 'error.html', {'message': 'Test not found.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving test: {str(e)}'})
    
    test_id = request.session['test_id']
    question_ids = request.session['question_ids']
    current_index = int(question_index)
    # Prevent navigation to previous questions
    session_current_index = request.session.get('current_index', 0)
    if current_index < session_current_index:
        return redirect('technical_test_page', question_index=session_current_index)
    
    if current_index < 0 or current_index >= len(question_ids):
        return redirect('submit_technical_test')
    
    try:
        question = Question.objects.get(question_id=question_ids[current_index])
        question_answer, created = TestUserQuestionAnswer.objects.get_or_create(
            user=user,
            test=test,
            question=question,
            defaults={
                'start_time': timezone.now(),
                'option_order': ','.join(['A', 'B', 'C', 'D'])  # Default option order
            }
        )
        # Update start_time if the record already exists
        if not created and not question_answer.start_time:
            question_answer.start_time = timezone.now()
            question_answer.save()
    except Question.DoesNotExist:
        return render(request, 'error.html', {'message': 'Question not found.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving question: {str(e)}'})
    
    # Fetch instructions for Technical Test
    try:
        instructions = Instruction.objects.filter(test_type='TT', is_active=True).order_by('display_order')
    except Exception as e:
        instructions = []
    
    remaining_seconds = request.session.get('remaining_seconds', test.duration_minutes * 60)
    current_time = timezone.now().timestamp()
    elapsed_time = current_time - request.session['start_time']
    remaining_seconds = max(0, remaining_seconds - elapsed_time)
    request.session['remaining_seconds'] = remaining_seconds
    request.session['start_time'] = current_time
    request.session['current_index'] = current_index  # Update current_index in session
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
        status = 'review' if mark_review else ('answered' if user_answer else 'not_answered')
        actual_answer = question.correct_answer if question.is_multichoice else question.technical_question_answer
        
        # Update current question's answer and timestamps
        question_answer.user_answer = user_answer
        question_answer.actual_answer = actual_answer
        question_answer.is_correct = user_answer == actual_answer if user_answer else None
        question_answer.score = 1 if user_answer == actual_answer else 0
        question_answer.status = status
        question_answer.submitted_at = timezone.now()
        question_answer.end_time = timezone.now()
        question_answer.save()
        
        # Update previous question's end_time if applicable
        if current_index > 0 and request.POST.get('action') == 'next':
            try:
                prev_question = Question.objects.get(question_id=question_ids[current_index - 1])
                prev_question_answer = TestUserQuestionAnswer.objects.get(
                    user=user, test=test, question=prev_question
                )
                if not prev_question_answer.end_time:
                    prev_question_answer.end_time = timezone.now()
                    prev_question_answer.save()
            except (Question.DoesNotExist, TestUserQuestionAnswer.DoesNotExist):
                pass  # Skip if previous question or answer record doesn't exist
        
        test.is_active = True
        test.save()
        
        action = request.POST.get('action')
        if action == 'next':
            next_index = current_index + 1
            if next_index < len(question_ids):
                return redirect('technical_test_page', question_index=next_index)
            else:
                return redirect('submit_technical_test')
        elif action == 'prev':
            prev_index = current_index - 1
            if prev_index >= 0:
                return redirect('technical_test_page', question_index=prev_index)
        elif action == 'submit':
            return redirect('submit_technical_test')
    
    answers = request.session.get('answers', {})
    marked_for_review = request.session.get('marked_for_review', {})
    saved_answer = answers.get(str(current_index), '')
    saved_review = marked_for_review.get(str(current_index), False)
    shuffled_options = question_answer.get_shuffled_options()
    context = {
        'question': question,
        'current_index': current_index,
        'total_questions': len(question_ids),
        'remaining_time': remaining_seconds,
        'answers': answers,
        'marked_for_review': marked_for_review,
        'question_range': range(len(question_ids)),
        'saved_answer': saved_answer,
        'saved_review': saved_review,
        'selected_language': request.session.get('selected_language'),
        'user': user,
        'shuffled_options': shuffled_options,
        'instructions': instructions,
        'test': test,
        'alert_duration' : get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
        'alert_cooldown' : get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
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
        # Update the current question's answer and timestamps
        current_index = request.session.get('current_index', 0)
        question_ids = request.session.get('question_ids', [])
        if current_index < len(question_ids):
            try:
                question = Question.objects.get(question_id=question_ids[current_index])
                question_answer = TestUserQuestionAnswer.objects.get(
                    user=user, test=test, question=question
                )
                user_answer = request.session.get('answers', {}).get(str(current_index), '')
                mark_review = request.session.get('marked_for_review', {}).get(str(current_index), False)
                status = 'review' if mark_review else ('answered' if user_answer else 'not_answered')
                actual_answer = question.correct_answer if question.is_multichoice else question.technical_question_answer
                
                question_answer.user_answer = user_answer
                question_answer.actual_answer = actual_answer
                question_answer.is_correct = user_answer == actual_answer if user_answer else None
                question_answer.score = 1 if user_answer == actual_answer else 0
                question_answer.status = status
                question_answer.submitted_at = current_time
                if not question_answer.start_time:  # Set start_time if not already set
                    question_answer.start_time = current_time
                question_answer.end_time = current_time
                question_answer.save()
            except (Question.DoesNotExist, TestUserQuestionAnswer.DoesNotExist):
                pass  # Skip if question or answer record doesn't exist
        test.is_active = False
        test.is_submitted = True
        test.submission_time = current_time
        test.test_status = 2  # Set test_status to 2 on submission
        suspicious_count = int(request.POST.get('suspicious_activity_count', test.suspicious_activity_count))
        test.suspicious_activity_count = suspicious_count
        test.save()
    except Tests.DoesNotExist:
        return render(request, 'error.html', {'message': 'Test not found.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error updating test: {str(e)}'})
    
    try:
        answers = TestUserQuestionAnswer.objects.filter(test=test)
        total_questions = get_config_value('tt_total_questions', 10, int)
        total_attempted = answers.exclude(user_answer='').count()
        total_correct = answers.filter(is_correct=True).count()
        percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
        cutoff_pass_score = get_config_value('tt_cutoff_pass_score', 5, int)
        Result.objects.update_or_create(
            test=test,
            user=test.user,
            defaults={
                'total_questions': total_questions,
                'total_attempted_questions': total_attempted,
                'total_correct_answers': total_correct,
                'percentage': percentage,
                'cutoff_pass_score': cutoff_pass_score,
                'skill': request.session.get('selected_language')
            }
        )
        # --- Send email to user after result is saved ---
        subject = "Submission Confirmation"
        to_email = [test.user.email]
        context = {
            'first_name': test.user.first_name,
            'test_name': test.test_name,
            'total_questions': total_questions,
            'total_attempted': total_attempted,
            'total_correct': total_correct,
            'percentage': percentage,
            'result_status': 'Pass' if total_correct >= cutoff_pass_score else 'Fail'
        }
        html_message = render_to_string('emails/technical_test_submitted.html', context)
        send_mail(
            subject,
            '',  # plain text message (optional)
            settings.DEFAULT_FROM_EMAIL,
            to_email,
            html_message=html_message,
            fail_silently=True
        )
        # Update submission_mail_sent field
        test.user.submission_mail_sent = True
        test.user.save()
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error saving test results: {str(e)}'})
    
    keys_to_clear = ['test_id', 'question_ids', 'current_index', 'answers', 'marked_for_review', 'start_time', 'remaining_seconds', 'original_start_time', 'selected_language']
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]
    request.session.modified = True
    
    messages.success(request, 'Technical Test submitted successfully!')
    if request.POST.get('action') == 'submit_and_logout':
        return redirect('user_logout')
    return redirect('test_selection')

@csrf_exempt
def update_resolution_mismatch(request):
    if request.method == 'POST':
        test_id = request.session.get('test_id')
        try:
            test = Tests.objects.get(test_id=test_id, user__user_id=request.session.get('user_id'))
            test.resolution_mismatch_count += 1
            test.save()
            response_data = {
                'status': 'success',
                'resolution_mismatch_count': test.resolution_mismatch_count,
                'auto_submit': test.resolution_mismatch_count >= 3
            }
            return JsonResponse(response_data)
        except Tests.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Test not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def captureScreenshot(request):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            photo_type = request.POST.get('photo_type')
            image_data = request.POST.get('image')
 
            if not user_id or not photo_type or not image_data:
                return JsonResponse({'success': False, 'error': 'Missing required parameters'}, status=400)
 
            if photo_type not in ['GT', 'TT', 'INST']:
                return JsonResponse({'success': False, 'error': 'Invalid photo type'}, status=400)
 
            user = Users.objects.get(user_id=user_id)
 
            # For GT and TT, verify an active test exists
            if photo_type in ['GT', 'TT']:
                test_id = request.session.get('test_id')
                if not test_id:
                    return JsonResponse({'success': False, 'error': 'No active test found'}, status=400)
                test = Tests.objects.get(test_id=test_id, user=user)
 
            # Decode base64 image data
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            if ext not in ['jpeg', 'jpg', 'png']:
                ext = 'jpg'
            data = base64.b64decode(imgstr)
 
            # Generate sequence number
            field_name = {'GT': 'gt_images', 'TT': 'tt_images', 'INST': 'inst_images'}[photo_type]
            current_images = getattr(user, field_name) or []
            sequence = len(current_images) + 1
 
            # Define file path
            registration_id = user.registration_id
            file_name = f"{registration_id}_verifiedexam_{photo_type}_{sequence}.{ext}"
            file_path = os.path.join('media', registration_id, 'Exam_images', file_name)
 
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
 
            # Save the file
            with open(file_path, 'wb') as f:
                f.write(data)
 
            # Update user's images field
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
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# @csrf_exempt
# def log_browser(request):
#     if request.method == 'POST':
#         user_agent = request.META.get('HTTP_USER_AGENT', '')
#         browser = 'Unknown Browser'

#         if 'Firefox' in user_agent:
#             browser = 'Mozilla Firefox'
#         elif 'Edg' in user_agent:
#             browser = 'Microsoft Edge'
#         elif 'Chrome' in user_agent:
#             browser = 'Google Chrome'
#         elif 'Safari' in user_agent:
#             browser = 'Apple Safari'

#         user_id = request.session.get('user_id')
#         if not user_id:
#             return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

#         try:
#             user = Users.objects.get(user_id=user_id)
#         except Users.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

#         test = Tests.objects.filter(user=user, is_submitted=False).order_by('-created_at').first()
#         if test:
#             test.browser_used = browser
#             test.save()
#             return JsonResponse({'status': 'success', 'browser': browser})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'No active test found'}, status=404)

#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)