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
import json
from datetime import datetime
from user_invite.models import UserInvite

import logging
logger = logging.getLogger(__name__)



# Global
current_year = datetime.now().year



# ==== Performance helpers injected for optimization ====
import random
from functools import lru_cache
from django.db import transaction
import threading
import base64
import os

# Optional: try to use Celery for async tasks (if configured). Otherwise fallback to immediate write.
try:
    from .tasks import save_screenshot_task, send_email_task  # user should implement tasks.py Celery tasks
    _HAS_CELERY = True
except Exception:
    _HAS_CELERY = False

@lru_cache(maxsize=512)
def _get_config_cached(config_key):
    try:
        return Configuration.objects.get(key=config_key, deleted=False).value
    except Configuration.DoesNotExist:
        return None

def get_config_value_cached(key, default=None, cast_type=None):
    """Cached wrapper around Configuration lookup (per-process)."""
    config_key = get_config_key_with_year(key)
    value = _get_config_cached(config_key)
    if value is None:
        value = _get_config_cached(key)
    if value is None:
        return default
    try:
        return cast_type(value) if cast_type else value
    except Exception:
        return default

def clear_config_cache():
    """Call this if you update configurations to clear the per-process cache."""
    _get_config_cached.cache_clear()

def sample_questions_by_id(test_type=None, difficulty=None, count=0, extra_filters=None):
    """Fetch ids for questions matching filters, sample ids, and return list of ids."""
    qs = Question.objects.filter(is_active=True, deleted=False)
    if test_type:
        qs = qs.filter(test_type=test_type)
    if difficulty:
        qs = qs.filter(difficulty=difficulty)
    if extra_filters:
        qs = qs.filter(**extra_filters)
    ids = list(qs.values_list('question_id', flat=True))
    if len(ids) < count:
        raise ValueError("Not enough questions")
    return random.sample(ids, count)

def fetch_questions_by_ids_in_order(ids):
    """Fetch Question objects for given ids and return in the same order as ids."""
    qs = Question.objects.filter(question_id__in=ids).only('question_id', 'correct_answer', 'is_multichoice', 'technical_question_answer')
    qmap = {q.question_id: q for q in qs}
    return [qmap[i] for i in ids]

def bulk_create_test_answers(user, test, questions):
    """Create TestUserQuestionAnswer rows in bulk for given question objects."""
    objs = []
    for q in questions:
        objs.append(TestUserQuestionAnswer(
            user=user, test=test, question=q, user_answer='',
            actual_answer=getattr(q, 'correct_answer', ''), is_correct=None, score=0,
            status='not_answered', submitted_at=None, end_time=None,
            option_order='A,B,C,D'
        ))
    TestUserQuestionAnswer.objects.bulk_create(objs)

def enqueue_screenshot_processing(user_id, photo_type, registration_id, data_bytes, ext):
    """Enqueue or write screenshot; returns file_path or None immediately."""
    # Prefer Celery task if present
    if _HAS_CELERY:
        # encode bytes to base64 string to send to Celery safely if needed
        save_screenshot_task.delay(user_id, photo_type, registration_id, base64.b64encode(data_bytes).decode(), ext)
        return None
    else:
        # fallback: write to media path quickly
        file_name = f"{registration_id}_verifiedexam_{photo_type}_{int(timezone.now().timestamp())}.{ext}"
        file_path = os.path.join('media', registration_id, 'Exam_images', file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(data_bytes)
        # Note: caller should update user model in a background task; here we return file_path
        return file_path

def send_mail_async(subject, message, from_email, recipient_list, fail_silently=True):
    """Send email via Celery if available, else send sync (consider short-circuiting in prod)."""
    if _HAS_CELERY:
        send_email_task.delay(subject, message, from_email, recipient_list, fail_silently)
    else:
        send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently)

# ==== end of injected helpers ====
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
    """Cached config lookup wrapper (per-process)."""
    return get_config_value_cached(key, default=default, cast_type=cast_type)


# ------------------------ Suspicious Activity ------------------------

# @csrf_exempt
# def update_suspicious_activity(request):
#     if request.method != 'POST':
#         return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

#     test_id = request.session.get('test_id')
#     person_count = int(request.POST.get('person_count', 0))
#     try:
#         test = Tests.objects.get(test_id=test_id, user__user_id=request.session.get('user_id'))
#         freeze_popup = auto_submit = False

#         if person_count == 0 or person_count > 1:
#             test.suspicious_activity_count += 1
#             test.save()

#             freeze_threshold = get_config_value('suspicious_activity_majorpopup', 3, int)
#             max_freeze_count = get_config_value('suspicious_activity_count', 9, int)

#             if test.suspicious_activity_count % freeze_threshold == 0 and test.suspicious_activity_count < max_freeze_count:
#                 freeze_popup = True
#             if test.suspicious_activity_count >= max_freeze_count:
#                 auto_submit = True

#         return JsonResponse({
#             'status': 'success',
#             'suspicious_activity_count': test.suspicious_activity_count,
#             'freeze_popup': freeze_popup,
#             'auto_submit': auto_submit,
#             'freeze_timer': get_config_value('freeze_Major_popup_timesec', 50, int)
#         })
#     except Tests.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': 'Test not found'}, status=404)


# ------------------------ General Test ------------------------

@login_required
def start_test(request):
    # Device restriction
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    ua = request.user_agent
    if ua.is_mobile or ua.is_tablet:
        return HttpResponseForbidden("Exams can only be taken on a Desktop device.")
    if ua.browser.family not in ["Chrome", "Firefox", "Edge"]:
        return HttpResponseForbidden("Please use Chrome, Firefox, or Edge on Desktop.")
    
    try:
        user = Users.objects.get(user_id=request.session['user_id'])
    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found. Please log in again.'}, status=400)

    # Prevent retake after submission
    if Tests.objects.filter(user=user, test_type='GT', is_submitted=True).exists():
        return JsonResponse({'error': 'You have already completed and submitted the General Test.'}, status=400)

    # Clear session
    for k in ['test_id', 'start_time', 'remaining_seconds', 'original_start_time']:
        request.session.pop(k, None)

    try:
        # ✅ Check if an active test already exists
        test = Tests.objects.filter(user=user, test_type='GT', is_submitted=False).first()

        if test:
            # Reuse existing test
            selected_ids = list(
                TestUserQuestionAnswer.objects.filter(test=test).values_list("question_id", flat=True)
            )
            # selected_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]  # temp
            questions = Question.objects.filter(question_id__in=selected_ids).values(
                'question_id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d',
                'correct_answer', 'is_multichoice', 'technical_question_answer'
            )
            # Maintain order
            question_map = {q['question_id']: q for q in questions}
            ordered_questions = [question_map[qid] for qid in selected_ids]
            if test.start_time is None:

                test.start_time = timezone.now()
                test.is_active = True

                test.end_time = test.start_time + timedelta(minutes=test.duration_minutes)

                test.save(update_fields=['start_time', 'end_time', 'is_active'])

        else:
            # ✅ Create a new test
            # Fetch question counts
            easy_count = get_config_value('gt_easy_questions', 10, int)
            med_count = get_config_value('gt_medium_questions', 10, int)
            hard_count = get_config_value('gt_hard_questions', 10, int)

            # Fetch question IDs
            easy_ids = list(Question.objects.filter(test_type='GT', difficulty='easy', is_active=True, deleted=False).values_list('question_id', flat=True))
            med_ids = list(Question.objects.filter(test_type='GT', difficulty='medium', is_active=True, deleted=False).values_list('question_id', flat=True))
            hard_ids = list(Question.objects.filter(test_type='GT', difficulty='hard', is_active=True, deleted=False).values_list('question_id', flat=True))

            if len(easy_ids) < easy_count or len(med_ids) < med_count or len(hard_ids) < hard_count:
                return JsonResponse({'error': 'Not enough questions to start the test.'}, status=400)

            selected_ids = (
                random.sample(easy_ids, easy_count) +
                random.sample(med_ids, med_count) +
                random.sample(hard_ids, hard_count)
            )
            # selected_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
            random.shuffle(selected_ids)

            questions = Question.objects.filter(question_id__in=selected_ids).values(
                'question_id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d',
                'correct_answer', 'is_multichoice', 'technical_question_answer'
            )
            question_map = {q['question_id']: q for q in questions}
            ordered_questions = [question_map[qid] for qid in selected_ids]

            duration = get_config_value('gt_duration_minutes', 30, int)
            test = Tests.objects.create(
                user=user, test_name="General Test", test_type='GT',
                duration_minutes=duration, start_time=timezone.now(),
                end_time=timezone.now() + timedelta(minutes=duration),
                is_active=True, is_submitted=False, suspicious_activity_count=0, test_status=1,
            )

            # Bulk create answer placeholders only for new test
            question_objects = Question.objects.filter(question_id__in=selected_ids)
            bulk_create_test_answers(user, test, question_objects)

        # Store minimal session data
        duration = test.duration_minutes
        request.session.update({
            'test_id': test.test_id,
            'start_time': test.start_time.timestamp(),
            'remaining_seconds': duration * 60,
            'original_start_time': test.start_time.timestamp()
        })
        request.session.modified = True

        return JsonResponse({
            'test_id': test.test_id,
            'questions': ordered_questions,
            'duration_seconds': duration * 60,
            'user': {'first_name': user.first_name},
            'instructions': list(
                Instruction.objects.filter(test_type='GT', is_active=True)
                .order_by('display_order')
                .values('title', 'content')
            )
        })

    except Exception as e:
        return JsonResponse({'error': f'Error creating new test: {e}'}, status=500)

def assign_test_questions(user_id):
    try:
        current_year = timezone.now().year
        try:
            user = Users.objects.get(user_id=user_id)
        except Users.DoesNotExist:
            return {'error': 'User not found.', 'status': 400}
 
        try:
            user_invite = UserInvite.objects.get(user=user)
            pre_assigned = user_invite.get_pre_assigned_questions()
            if pre_assigned.get('GT'):
                return {
                    'success': True,
                    'message': f'Questions already pre-assigned for {user.email} (GT: {len(pre_assigned.get("GT", []))}).'
                }
        except UserInvite.DoesNotExist:
            user_invite, _ = UserInvite.objects.get_or_create(user=user)
 
        if Tests.objects.filter(user=user, test_type='GT', is_submitted=True).exists():
            return {'error': 'User has completed the General Test.', 'status': 400}
 
        # Fetch GT question counts from config_keys
        easy_count = get_config_value(f'gt_easy_questions_{current_year}', 6, int)
        med_count = get_config_value(f'gt_medium_questions_{current_year}', 7, int)
        hard_count = get_config_value(f'gt_hard_questions_{current_year}', 7, int)
        total_questions = get_config_value(f'gt_total_questions_{current_year}', 20, int)
 
        # Validate total questions
        if easy_count + med_count + hard_count != total_questions:
            return {
                'error': f'Total GT questions mismatch (easy: {easy_count}, medium: {med_count}, hard: {hard_count}, expected total: {total_questions}).',
                'status': 400
            }
 
        # Fetch GT question IDs
        easy_ids = list(Question.objects.filter(
            test_type='GT', difficulty='easy', is_active=True, deleted=False
        ).values_list('question_id', flat=True))
        med_ids = list(Question.objects.filter(
            test_type='GT', difficulty='medium', is_active=True, deleted=False
        ).values_list('question_id', flat=True))
        hard_ids = list(Question.objects.filter(
            test_type='GT', difficulty='hard', is_active=True, deleted=False
        ).values_list('question_id', flat=True))
 
        # Validate question availability
        if len(easy_ids) < easy_count or len(med_ids) < med_count or len(hard_ids) < hard_count:
            return {
                'error': f'Not enough GT questions (easy: {len(easy_ids)}/{easy_count}, medium: {len(med_ids)}/{med_count}, hard: {len(hard_ids)}/{hard_count}).',
                'status': 400
            }
 
        # Select questions
        selected_ids = (
            random.sample(easy_ids, easy_count) +
            random.sample(med_ids, med_count) +
            random.sample(hard_ids, hard_count) if hard_count > 0 else []
        )
        random.shuffle(selected_ids)
 
        # Verify selected questions
        questions = Question.objects.filter(
            question_id__in=selected_ids, test_type='GT', is_active=True, deleted=False
        )
        if questions.count() != total_questions:
            return {
                'error': f'Not enough valid GT questions (available: {questions.count()}, required: {total_questions}).',
                'status': 400
            }
 
        # Create Tests record
        duration = get_config_value(f'gt_duration_minutes_{current_year}', 30, int)
        try:
            test = Tests.objects.create(
                user=user,
                test_name="General Test",
                test_type='GT',
                duration_minutes=duration,
                is_submitted=False,
                is_active=False,
                suspicious_activity_count=0,
                test_status=0,
                resolution_mismatch_count=0,
                created_at=timezone.now(),
                # start_time and end_time left as NULL
            )
            logger.info(f"Created Tests record for {user.email}, test_type=GT, test_id={test.test_id}")
        except Exception as e:
            return {'error': f'Error creating Tests record: {str(e)}', 'status': 500}
 
        # Create TestUserQuestionAnswer records
        try:
            bulk_create_test_answers(user, test, questions)
            logger.info(f"Created {len(selected_ids)} TestUserQuestionAnswer records for {user.email}, test_type=GT")
        except Exception as e:
            test.delete()  # Rollback Tests record
            return {'error': f'Error creating TestUserQuestionAnswer records: {str(e)}', 'status': 500}
 
        # Store pre-assigned questions
        try:
            user_invite.set_pre_assigned_questions({'GT': selected_ids})
            return {
                'success': True,
                'user_id': user.user_id,
                'message': f'Questions pre-assigned and records created for {user.email} (GT: {len(selected_ids)}).'
            }
        except Exception as e:
            test.delete()  # Rollback Tests record
            TestUserQuestionAnswer.objects.filter(test=test).delete()  # Rollback answers
            return {'error': f'Error storing pre-assigned questions: {str(e)}', 'status': 500}
 
    except Exception as e:
        return {'error': f'Error pre-assigning questions: {str(e)}', 'status': 500}
@login_required
def test_page(request):
    try:
        user = Users.objects.get(user_id=request.session['user_id'])
    except Users.DoesNotExist:
        return redirect('user_login')

    if 'test_id' not in request.session:
        return redirect('start_test')

    try:
        test = Tests.objects.get(test_id=request.session['test_id'])
    except Tests.DoesNotExist:
        return render(request, 'error.html', {'message': 'Test not found.'})

    context = {
        'test': test,
        'user': user,
        'alert_duration': get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
        'alert_cooldown': get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
        # 👇 these replace update_suspicious_activity view
        'freeze_threshold': get_config_value('suspicious_activity_majorpopup', 3, int),
        'max_freeze_count': get_config_value('suspicious_activity_count', 9, int),
        'freeze_timer': get_config_value('freeze_Major_popup_timesec', 50, int),
        # 👇 new config for resolution mismatches
        'max_resolution_mismatches': get_config_value('resolution_mismatch_count', 3, int),
    }

    return render(request, 'test_page.html', context)

@login_required
# def submit_test(request):
#     if 'test_id' not in request.session:
#         return JsonResponse({'error': 'No active test found.'}, status=400)

#     try:
#         test = Tests.objects.get(test_id=request.session['test_id'])
#         user = Users.objects.get(user_id=request.session['user_id'])
#         current_time = timezone.now()

#         if request.method == 'POST':
#             data = json.loads(request.body)
#             answers = data.get('answers', {})
#             suspicious_activity_count = data.get(
#                 'suspicious_activity_count', test.suspicious_activity_count
#             )
#             resolution_mismatch_count = data.get(
#                 'resolution_mismatch_count', test.resolution_mismatch_count
#             )

#             # ✅ Get all questions assigned to this test
#             all_questions = Question.objects.filter(
#                 testuserquestionanswer__test=test
#             ).distinct()

#             # Process answers atomically
#             with transaction.atomic():
#                 for question in all_questions:
#                     answer_data = None
#                     # Find matching answer from frontend (if any)
#                     for idx, val in answers.items():
#                         if str(val.get('question_id')) == str(question.question_id):
#                             answer_data = val
#                             break

#                     if answer_data:
#                         user_answer = answer_data.get('user_answer', '')
#                         mark_review = answer_data.get('mark_review', False)
#                         status = (
#                             'review' if mark_review
#                             else ('answered' if user_answer else 'not_answered')
#                         )
#                     else:
#                         # Not attempted → store explicitly
#                         user_answer = ''
#                         mark_review = False
#                         status = 'not_answered'

#                     TestUserQuestionAnswer.objects.update_or_create(
#                         user=user,
#                         test=test,
#                         question=question,
#                         defaults={
#                             'user_answer': user_answer,
#                             'actual_answer': question.correct_answer,
#                             'is_correct': (
#                                 user_answer == question.correct_answer
#                                 if user_answer else None
#                             ),
#                             'score': 1 if user_answer == question.correct_answer else 0,
#                             'status': status,
#                             'submitted_at': timezone.now(),
#                             'end_time': timezone.now(),
#                         }
#                     )

#         # Update test status
#         test.is_active = False
#         test.is_submitted = True
#         test.submission_time = current_time
#         test.test_status = 2
#         test.suspicious_activity_count = suspicious_activity_count
#         test.resolution_mismatch_count = resolution_mismatch_count
#         test.save()

#         # Compute results
#         answers_qs = TestUserQuestionAnswer.objects.filter(test=test)
#         total_questions = get_config_value('gt_total_questions', 30, int)
#         total_attempted = answers_qs.exclude(user_answer='').count()
#         total_correct = answers_qs.filter(is_correct=True).count()
#         percentage = (total_correct / total_questions * 100) if total_questions else 0
#         cutoff = get_config_value('gt_cutoff_pass_score', 15, int)
#         result_status = 'pass' if total_correct >= cutoff else 'fail'

#         Result.objects.update_or_create(
#             test=test,
#             user=user,
#             defaults=dict(
#                 total_questions=total_questions,
#                 total_attempted_questions=total_attempted,
#                 total_correct_answers=total_correct,
#                 percentage=percentage,
#                 cutoff_pass_score=cutoff,
#                 result_status=result_status,
#             )
#         )

#         # Clear session
#         for k in ['test_id', 'start_time', 'remaining_seconds', 'original_start_time']:
#             request.session.pop(k, None)
#         request.session.modified = True

#         return JsonResponse(
#             {'status': 'success', 'message': 'General Test submitted successfully!'}
#         )

#     except Exception as e:
#         return JsonResponse({'error': f'Error submitting test: {e}'}, status=500)


def submit_test(request):
    if 'test_id' not in request.session:
        return JsonResponse({'error': 'No active test found.'}, status=400)

    try:
        test = Tests.objects.get(test_id=request.session['test_id'])
        user = Users.objects.get(user_id=request.session['user_id'])
        current_time = datetime.now()  # ✅ naive datetime since USE_TZ=False

        if request.method == 'POST':
            data = json.loads(request.body)
            answers = data.get('answers', {})
            suspicious_activity_count = data.get(
                'suspicious_activity_count', test.suspicious_activity_count
            )
            resolution_mismatch_count = data.get(
                'resolution_mismatch_count', test.resolution_mismatch_count
            )

            all_questions = Question.objects.filter(
                testuserquestionanswer__test=test
            ).distinct()

            to_create, to_update = [], []

            with transaction.atomic():
                existing_answers = {
                    a.question_id: a
                    for a in TestUserQuestionAnswer.objects.filter(test=test, user=user)
                }

                for question in all_questions:
                    # Find frontend answer for this question
                    answer_data = next(
                        (val for val in answers.values()
                         if str(val.get('question_id')) == str(question.question_id)),
                        None
                    )

                    if answer_data:
                        user_answer = answer_data.get('user_answer', '')
                        mark_review = answer_data.get('mark_review', False)

                        # ✅ Parse start_time / end_time safely
                        start_time_str = answer_data.get('start_time')
                        end_time_str = answer_data.get('end_time')
                        OFFSET = timedelta(hours=5, minutes=30)

                        def parse_iso(s):
                            if not s:
                                return None
                            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
                            return (dt + OFFSET).replace(tzinfo=None)

                        start_time = parse_iso(start_time_str)
                        end_time = parse_iso(end_time_str)

                        status = (
                            'review' if mark_review
                            else ('answered' if user_answer else 'not_answered')
                        )
                    else:
                        user_answer = ''
                        mark_review = False
                        start_time, end_time = None, None
                        status = 'not_answered'

                    # Prepare object (new or update)
                    if question.question_id in existing_answers:
                        obj = existing_answers[question.question_id]
                        obj.user_answer = user_answer
                        obj.actual_answer = question.correct_answer
                        obj.is_correct = (
                            user_answer == question.correct_answer if user_answer else None
                        )
                        obj.score = 1 if user_answer == question.correct_answer else 0
                        obj.status = status
                        obj.start_time = start_time
                        obj.end_time = end_time
                        obj.submitted_at = current_time
                        to_update.append(obj)
                    else:
                        to_create.append(TestUserQuestionAnswer(
                            user=user,
                            test=test,
                            question=question,
                            user_answer=user_answer,
                            actual_answer=question.correct_answer,
                            is_correct=(
                                user_answer == question.correct_answer if user_answer else None
                            ),
                            score=1 if user_answer == question.correct_answer else 0,
                            status=status,
                            start_time=start_time,
                            end_time=end_time,
                            submitted_at=current_time,
                        ))

                # ✅ Bulk insert & update
                if to_create:
                    TestUserQuestionAnswer.objects.bulk_create(to_create, batch_size=20)
                if to_update:
                    TestUserQuestionAnswer.objects.bulk_update(
                        to_update,
                        fields=[
                            'user_answer', 'actual_answer', 'is_correct', 'score',
                            'status', 'start_time', 'end_time', 'submitted_at'
                        ],
                        batch_size=20
                    )

            # ✅ Update test status
            test.is_active = False
            test.is_submitted = True
            test.submission_time = current_time
            test.test_status = 2
            test.suspicious_activity_count = suspicious_activity_count
            test.resolution_mismatch_count = resolution_mismatch_count
            test.save()

            # ✅ Compute results
            answers_qs = TestUserQuestionAnswer.objects.filter(test=test)
            total_questions = get_config_value('gt_total_questions', 30, int)
            total_attempted = answers_qs.exclude(user_answer='').count()
            total_correct = answers_qs.filter(is_correct=True).count()
            percentage = (total_correct / total_questions * 100) if total_questions else 0
            cutoff = get_config_value('gt_cutoff_pass_score', 15, int)
            result_status = 'pass' if total_correct >= cutoff else 'fail'

            Result.objects.update_or_create(
                test=test,
                user=user,
                defaults=dict(
                    total_questions=total_questions,
                    total_attempted_questions=total_attempted,
                    total_correct_answers=total_correct,
                    percentage=percentage,
                    cutoff_pass_score=cutoff,
                    result_status=result_status,
                )
            )

            # ✅ Clear session
            for k in ['test_id', 'start_time', 'remaining_seconds', 'original_start_time']:
                request.session.pop(k, None)
            request.session.modified = True

            return JsonResponse(
                {'status': 'success', 'message': 'General Test submitted successfully!'}
            )

    except Exception as e:
        return JsonResponse({'error': f'Error submitting test: {e}'}, status=500)


# --- VIEW 1: render language selection (unchanged except clearing old TT session keys) ---
@login_required
def select_language(request):
    try:
        user = Users.objects.get(user_id=request.session['user_id'])
    except Users.DoesNotExist:
        return redirect('user_login')

    # Prevent starting a new test if one is already submitted
    if Tests.objects.filter(user=user, test_type='TT', is_submitted=True).exists():
        # You might want to redirect to a dashboard or a page showing results
        return render(request, 'error.html', {'message': 'You have already completed the technical test.'})
    
    if Tests.objects.filter(user=user, test_type='TT').exists():
        # You might want to redirect to a dashboard or a page showing results
        return render(request, 'error.html', {'message': 'You have already assigned the technical test.'})

    # Clear old technical test session data just in case
    for k in ['tt_test_id', 'tt_start_time', 'tt_remaining_seconds', 'selected_language']:
        request.session.pop(k, None)

    try:
        config_key = get_config_key_with_year('programming_languages')
        languages = Configuration.objects.filter(key=config_key, deleted=False).values_list('value', flat=True)
        if not languages:
            return render(request, 'error.html', {'message': 'No programming languages configured.'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error retrieving languages: {e}'})

    # This view now ONLY renders the template. The form submission is handled by JavaScript.
    return render(request, 'select_language.html', {'languages': languages})


# --- VIEW 2: API Endpoint to create the test and return data ---
@login_required
def start_technical_test(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    ua = request.user_agent
    if ua.is_mobile or ua.is_tablet:
        return JsonResponse({'error': 'Exams can only be taken on a Desktop device.'}, status=403)
    if ua.browser.family not in ["Chrome", "Firefox", "Edge"]:
        return JsonResponse({'error': 'Please use Chrome, Firefox, or Edge on Desktop.'}, status=403)

    try:
        user = Users.objects.get(user_id=request.session['user_id'])
        data = json.loads(request.body)
        selected_language = data.get('language')
    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found. Please log in again.'}, status=400)
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request body.'}, status=400)

    if not selected_language:
        return JsonResponse({'error': 'Language not provided.'}, status=400)

    # Prevent retake after submission
    if Tests.objects.filter(user=user, test_type='TT', is_submitted=True, test_name__icontains=selected_language).exists():
        return JsonResponse({'error': f'You have already completed the Technical Test for {selected_language}.'}, status=400)

    # Clear session to ensure a clean start
    for k in ['tt_test_id', 'tt_start_time', 'tt_remaining_seconds', 'original_start_time']:
        request.session.pop(k, None)

    try:
        # If an active test exists, resume it
        test = Tests.objects.filter(user=user, test_type='TT', test_name__icontains=selected_language, is_active=True, is_submitted=False).first()

        if test:
            # resumed order: use attempt_id (your PK) — previously caused "id" error
            selected_ids = list(
                TestUserQuestionAnswer.objects.filter(test=test)
                .order_by('attempt_id')
                .values_list("question_id", flat=True)
            )
            # selected_ids = [2447,2448,2449,2450,2451,2452,2453,2454,2455,2456,2457,2458,2459,2460,2461,2462,2463,2464,2465,2466]  
            questions = Question.objects.filter(question_id__in=selected_ids).values(
                'question_id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d',
                'correct_answer', 'is_multichoice', 'technical_question_answer'
            )
            question_map = {q['question_id']: q for q in questions}
            ordered_questions = [question_map[qid] for qid in selected_ids if qid in question_map]
        else:
            # config counts
            easy_coding_count = get_config_value('tt_coding_easy_questions', 2, int)
            medium_coding_count = get_config_value('tt_coding_medium_questions', 1, int)
            hard_coding_count = get_config_value('tt_coding_hard_questions', 1, int)
            easy_mcq_count = get_config_value('tt_mcq_easy_questions', 2, int)
            medium_mcq_count = get_config_value('tt_mcq_medium_questions', 2, int)
            hard_mcq_count = get_config_value('tt_mcq_hard_questions', 2, int)

            # use case-insensitive match for specialisation_name
            easy_coding_ids = list(Question.objects.filter(
                test_type='TT', difficulty='easy',
                specialisation_name__iexact=selected_language,
                is_multichoice=False, is_active=True, deleted=False
            ).values_list('question_id', flat=True))
            medium_coding_ids = list(Question.objects.filter(
                test_type='TT', difficulty='medium',
                specialisation_name__iexact=selected_language,
                is_multichoice=False, is_active=True, deleted=False
            ).values_list('question_id', flat=True))
            hard_coding_ids = list(Question.objects.filter(
                test_type='TT', difficulty='hard',
                specialisation_name__iexact=selected_language,
                is_multichoice=False, is_active=True, deleted=False
            ).values_list('question_id', flat=True))
            easy_mcq_ids = list(Question.objects.filter(
                test_type='TT', difficulty='easy',
                specialisation_name__iexact=selected_language,
                is_multichoice=True, is_active=True, deleted=False
            ).values_list('question_id', flat=True))
            medium_mcq_ids = list(Question.objects.filter(
                test_type='TT', difficulty='medium',
                specialisation_name__iexact=selected_language,
                is_multichoice=True, is_active=True, deleted=False
            ).values_list('question_id', flat=True))
            hard_mcq_ids = list(Question.objects.filter(
                test_type='TT', difficulty='hard',
                specialisation_name__iexact=selected_language,
                is_multichoice=True, is_active=True, deleted=False
            ).values_list('question_id', flat=True))

            # quick diagnostic: return counts if not enough
            missing_buckets = []
            if len(easy_coding_ids) < easy_coding_count:
                missing_buckets.append({'bucket': 'easy_coding', 'have': len(easy_coding_ids), 'need': easy_coding_count})
            if len(medium_coding_ids) < medium_coding_count:
                missing_buckets.append({'bucket': 'medium_coding', 'have': len(medium_coding_ids), 'need': medium_coding_count})
            if len(hard_coding_ids) < hard_coding_count:
                missing_buckets.append({'bucket': 'hard_coding', 'have': len(hard_coding_ids), 'need': hard_coding_count})
            if len(easy_mcq_ids) < easy_mcq_count:
                missing_buckets.append({'bucket': 'easy_mcq', 'have': len(easy_mcq_ids), 'need': easy_mcq_count})
            if len(medium_mcq_ids) < medium_mcq_count:
                missing_buckets.append({'bucket': 'medium_mcq', 'have': len(medium_mcq_ids), 'need': medium_mcq_count})
            if len(hard_mcq_ids) < hard_mcq_count:
                missing_buckets.append({'bucket': 'hard_mcq', 'have': len(hard_mcq_ids), 'need': hard_mcq_count})

            if missing_buckets:
                # return helpful info to frontend so you can see what's missing
                return JsonResponse({
                    'error': f'Not enough questions for {selected_language}.',
                    'missing': missing_buckets
                }, status=400)

            selected_ids = (
                random.sample(easy_coding_ids, easy_coding_count) +
                random.sample(medium_coding_ids, medium_coding_count) +
                random.sample(hard_coding_ids, hard_coding_count) +
                random.sample(easy_mcq_ids, easy_mcq_count) +
                random.sample(medium_mcq_ids, medium_mcq_count) +
                random.sample(hard_mcq_ids, hard_mcq_count)
            )
            # selected_ids = [2447,2448,2449,2450,2451,2452,2453,2454,2455,2456,2457,2458,2459,2460,2461,2462,2463,2464,2465,2466]
            random.shuffle(selected_ids)

            questions = Question.objects.filter(question_id__in=selected_ids).values(
                'question_id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d',
                'correct_answer', 'is_multichoice', 'technical_question_answer'
            )
            question_map = {q['question_id']: q for q in questions}
            ordered_questions = [question_map[qid] for qid in selected_ids if qid in question_map]

            duration = get_config_value('tt_duration_minutes', 30, int)
            test = Tests.objects.create(
                user=user, test_name=f"Technical Test - {selected_language}", test_type='TT',
                duration_minutes=duration, start_time=timezone.now(),
                end_time=timezone.now() + timedelta(minutes=duration),
                is_active=True, is_submitted=False, suspicious_activity_count=0, test_status=1
            )

            # create TestUserQuestionAnswer rows
            question_objects = Question.objects.filter(question_id__in=selected_ids)
            # If your helper expects ordered_questions list, pass that. Ensure bulk_create_test_answers respects order.
            bulk_create_test_answers(user, test, question_objects)

        duration = test.duration_minutes
        request.session.update({
            'tt_test_id': test.test_id,
            'tt_start_time': test.start_time.timestamp(),
            'tt_remaining_seconds': duration * 60,
            'original_start_time': test.start_time.timestamp(),
            'selected_language': selected_language
        })
        request.session.modified = True

        return JsonResponse({
            'test_id': test.test_id,
            'questions': ordered_questions,
            'duration_seconds': duration * 60,
            'user': {'first_name': user.first_name},
            'selected_language': selected_language,
            'instructions': list(
                Instruction.objects.filter(test_type='TT', is_active=True)
                .order_by('display_order')
                .values('title', 'content')
            )
        })

    except Exception as e:
        return JsonResponse({'error': f'Error creating new technical test: {e}'}, status=500)



# --- VIEW 3: Renders the HTML shell for the test page ---
@login_required
def technical_test_page(request):
    # SPA shell — frontend JS will read questions from sessionStorage (sent by start_technical_test)
    if 'tt_test_id' not in request.session:
        return redirect('select_language')

    try:
        test = Tests.objects.get(test_id=request.session['tt_test_id'])
        user = Users.objects.get(user_id=request.session['user_id'])
    except (Tests.DoesNotExist, Users.DoesNotExist):
        request.session.pop('tt_test_id', None)
        return redirect('select_language')

    # derive total_questions from TestUserQuestionAnswer rows for the test (reliable)
    total_questions = TestUserQuestionAnswer.objects.filter(test=test).count()

    context = {
        'test': test,
        'user': user,
        'selected_language': request.session.get('selected_language', ''),
        'total_questions': total_questions,
        'alert_duration': get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
        'alert_cooldown': get_config_value('freeze_Small_popup_timesec', 15, int) * 1000,
        # 👇 these replace update_suspicious_activity view
        'freeze_threshold': get_config_value('suspicious_activity_majorpopup', 3, int),
        'max_freeze_count': get_config_value('suspicious_activity_count', 9, int),
        'freeze_timer': get_config_value('freeze_Major_popup_timesec', 50, int),
        # 👇 new config for resolution mismatches
        'max_resolution_mismatches': get_config_value('resolution_mismatch_count', 3, int),
    }
    return render(request, 'technical_test_page.html', context)



# --- VIEW 4: API Endpoint to submit the test ---
@login_required
# def submit_technical_test(request):
#     # This view is now a pure API endpoint
#     if 'tt_test_id' not in request.session:
#         return JsonResponse({'error': 'No active test found.'}, status=400)

#     try:
#         test = Tests.objects.get(test_id=request.session['tt_test_id'])
#         user = Users.objects.get(user_id=request.session['user_id'])
#         current_time = timezone.now()

#         if request.method == 'POST':
#             data = json.loads(request.body)
#             answers = data.get('answers', {})
#             suspicious_activity_count = data.get('suspicious_activity_count', test.suspicious_activity_count)
#             resolution_mismatch_count = data.get('resolution_mismatch_count', test.resolution_mismatch_count)

#             all_questions = Question.objects.filter(testuserquestionanswer__test=test).distinct()

#             with transaction.atomic():
#                 for question in all_questions:
#                     answer_data = answers.get(str(question.question_id))

#                     if answer_data:
#                         user_answer = answer_data.get('user_answer', '')
#                         mark_review = answer_data.get('mark_review', False)
#                         status = 'review' if mark_review else ('answered' if user_answer else 'not_answered')
#                     else:
#                         user_answer, mark_review, status = '', False, 'not_answered'

#                     actual_answer = question.correct_answer if question.is_multichoice else question.technical_question_answer

#                     TestUserQuestionAnswer.objects.update_or_create(
#                         user=user, test=test, question=question,
#                         defaults={
#                             'user_answer': user_answer,
#                             'actual_answer': actual_answer,
#                             'is_correct': (user_answer == actual_answer if user_answer else None),
#                             'score': 1 if user_answer == actual_answer else 0,
#                             'status': status,
#                             'submitted_at': timezone.now(),
#                             'end_time': timezone.now()
#                         }
#                     )

#             # Update test status
#             test.is_active = False
#             test.is_submitted = True
#             test.submission_time = current_time
#             test.test_status = 2
#             test.suspicious_activity_count = suspicious_activity_count
#             test.resolution_mismatch_count = resolution_mismatch_count
#             test.save()

#             # Compute results
#             answers_qs = TestUserQuestionAnswer.objects.filter(test=test)
#             total_questions = get_config_value('tt_total_questions', 10, int)
#             total_attempted = answers_qs.exclude(user_answer='').count()
#             total_correct = answers_qs.filter(is_correct=True).count()
#             percentage = (total_correct / total_questions * 100) if total_questions else 0
#             cutoff = get_config_value('tt_cutoff_pass_score', 5, int)
#             result_status = 'pass' if total_correct >= cutoff else 'fail'

#             Result.objects.update_or_create(
#                 test=test, user=user,
#                 defaults=dict(
#                     total_questions=total_questions,
#                     total_attempted_questions=total_attempted,
#                     total_correct_answers=total_correct,
#                     percentage=percentage,
#                     cutoff_pass_score=cutoff,
#                     skill=request.session.get('selected_language'),
#                     result_status=result_status
#                 )
#             )

#             # Optional: send confirmation email (uncomment if you want mail behavior like old view)
#             # try:
#             #     subject = "Submission Confirmation"
#             #     to_email = [user.email]
#             #     context = {
#             #         'first_name': user.first_name,
#             #         'test_name': test.test_name,
#             #         'total_questions': total_questions,
#             #         'total_attempted': total_attempted,
#             #         'total_correct': total_correct,
#             #         'percentage': percentage,
#             #         'result_status': 'Pass' if total_correct >= cutoff else 'Fail'
#             #     }
#             #     html_message = render_to_string('emails/technical_test_submitted.html', context)
#             #     send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, to_email, html_message=html_message, fail_silently=True)
#             #     user.submission_mail_sent = True
#             #     user.save()
#             # except Exception:
#             #     pass

#             # Clear session keys
#             for k in ['tt_test_id', 'tt_start_time', 'tt_remaining_seconds', 'original_start_time', 'selected_language']:
#                 request.session.pop(k, None)
#             request.session.modified = True

#             return JsonResponse({'status': 'success', 'message': 'Technical Test submitted successfully!'})

#     except Exception as e:
#         return JsonResponse({'error': f'Error submitting test: {e}'}, status=500)


def submit_technical_test(request):
    if 'tt_test_id' not in request.session:
        return JsonResponse({'error': 'No active test found.'}, status=400)

    try:
        test = Tests.objects.get(test_id=request.session['tt_test_id'])
        user = Users.objects.get(user_id=request.session['user_id'])
        current_time = timezone.now()

        if request.method == 'POST':
            data = json.loads(request.body)
            answers = data.get('answers', {})
            suspicious_activity_count = data.get(
                'suspicious_activity_count', test.suspicious_activity_count
            )
            resolution_mismatch_count = data.get(
                'resolution_mismatch_count', test.resolution_mismatch_count
            )

            all_questions = Question.objects.filter(
                testuserquestionanswer__test=test
            ).distinct()

            to_create, to_update = [], []

            with transaction.atomic():
                # Cache existing answers
                existing_answers = {
                    a.question_id: a
                    for a in TestUserQuestionAnswer.objects.filter(test=test, user=user)
                }

                for question in all_questions:
                    answer_data = answers.get(str(question.question_id))

                    if answer_data:
                        user_answer = answer_data.get('user_answer', '')
                        mark_review = answer_data.get('mark_review', False)
                        # Parse start_time / end_time safely
                        start_time_str = answer_data.get('start_time')
                        end_time_str = answer_data.get('end_time')
                        OFFSET = timedelta(hours=5, minutes=30)

                        def parse_iso(s):
                            if not s:
                                return None
                            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
                            return (dt + OFFSET).replace(tzinfo=None)

                        start_time = parse_iso(start_time_str)
                        end_time = parse_iso(end_time_str)

                        status = (
                            'review' if mark_review
                            else ('answered' if user_answer else 'not_answered')
                        )
                    else:
                        user_answer, mark_review, start_time, end_time = '', False, None, None
                        status = 'not_answered'

                    # Choose correct reference answer
                    actual_answer = (
                        question.correct_answer if question.is_multichoice
                        else question.technical_question_answer
                    )

                    if question.question_id in existing_answers:
                        obj = existing_answers[question.question_id]
                        obj.user_answer = user_answer
                        obj.actual_answer = actual_answer
                        obj.is_correct = (
                            user_answer == actual_answer if user_answer else None
                        )
                        obj.score = 1 if user_answer == actual_answer else 0
                        obj.status = status
                        obj.start_time = start_time
                        obj.end_time = end_time
                        obj.submitted_at = current_time
                        to_update.append(obj)
                    else:
                        to_create.append(TestUserQuestionAnswer(
                            user=user,
                            test=test,
                            question=question,
                            user_answer=user_answer,
                            actual_answer=actual_answer,
                            is_correct=(
                                user_answer == actual_answer if user_answer else None
                            ),
                            score=1 if user_answer == actual_answer else 0,
                            status=status,
                            start_time=start_time,
                            end_time=end_time,
                            submitted_at=current_time,
                        ))

                # Bulk operations (batch_size = 20)
                if to_create:
                    TestUserQuestionAnswer.objects.bulk_create(to_create, batch_size=20)
                if to_update:
                    TestUserQuestionAnswer.objects.bulk_update(
                        to_update,
                        fields=[
                            'user_answer', 'actual_answer', 'is_correct', 'score',
                            'status', 'start_time', 'end_time', 'submitted_at'
                        ],
                        batch_size=20
                    )

            # Update test status
            test.is_active = False
            test.is_submitted = True
            test.submission_time = current_time
            test.test_status = 2
            test.suspicious_activity_count = suspicious_activity_count
            test.resolution_mismatch_count = resolution_mismatch_count
            test.save()

            # Compute results
            answers_qs = TestUserQuestionAnswer.objects.filter(test=test)
            total_questions = get_config_value('tt_total_questions', 10, int)
            total_attempted = answers_qs.exclude(user_answer='').count()
            total_correct = answers_qs.filter(is_correct=True).count()
            percentage = (total_correct / total_questions * 100) if total_questions else 0
            cutoff = get_config_value('tt_cutoff_pass_score', 5, int)
            result_status = 'pass' if total_correct >= cutoff else 'fail'

            Result.objects.update_or_create(
                test=test,
                user=user,
                defaults=dict(
                    total_questions=total_questions,
                    total_attempted_questions=total_attempted,
                    total_correct_answers=total_correct,
                    percentage=percentage,
                    cutoff_pass_score=cutoff,
                    skill=request.session.get('selected_language'),
                    result_status=result_status,
                )
            )

            # Optional: send confirmation email (uncomment if you want mail behavior like old view)
            try:
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
                send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, to_email, html_message=html_message, fail_silently=True)
                user.submission_mail_sent = True
                user.save()
            except Exception:
                pass

            # Clear session
            for k in [
                'tt_test_id', 'tt_start_time',
                'tt_remaining_seconds', 'original_start_time',
                'selected_language'
            ]:
                request.session.pop(k, None)
            request.session.modified = True

            return JsonResponse(
                {'status': 'success', 'message': 'Technical Test submitted successfully!'}
            )

    except Exception as e:
        return JsonResponse({'error': f'Error submitting test: {e}'}, status=500)


# ------------------------ Resolution Mismatch ------------------------

# @csrf_exempt
# def update_resolution_mismatch(request):
#     if request.method != 'POST':
#         return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

#     test_id = request.session.get('test_id')
#     try:
#         test = Tests.objects.get(test_id=test_id, user__user_id=request.session.get('user_id'))
#         test.resolution_mismatch_count += 1
#         test.save()
#         return JsonResponse({
#             'status': 'success',
#             'resolution_mismatch_count': test.resolution_mismatch_count,
#             'auto_submit': test.resolution_mismatch_count >= 3
#         })
#     except Tests.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': 'Test not found'}, status=404)


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

        registration_id = user.registration_id

        # enqueue or write screenshot quickly; may return file_path if written synchronously
        file_path = enqueue_screenshot_processing(user.user_id, photo_type, registration_id, data, ext)

        if file_path:
            # fallback: update user model immediately
            field_name = {'GT': 'gt_images', 'TT': 'tt_images', 'INST': 'inst_images'}[photo_type]
            current_images = getattr(user, field_name) or []
            current_images.append(file_path)
            setattr(user, field_name, current_images)
            user.save()
            return JsonResponse({'success': True, 'message': 'Screenshot saved (fallback).'})
        else:
            # processed/queued by background worker
            return JsonResponse({'success': True, 'message': 'Screenshot queued for processing.'})
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    except Tests.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Test not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



@csrf_exempt
def log_browser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            browser = data.get('browser', 'Unknown Browser')
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

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
