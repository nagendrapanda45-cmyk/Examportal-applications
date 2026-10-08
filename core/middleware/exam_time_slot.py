from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from user_invite.models import UserInvite
from home.users.models import Users, Configuration
from datetime import datetime, timedelta
import logging
import re

logger = logging.getLogger(__name__)

class ExamTimeSlotMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = [
            '/candidates/login/',
            '/candidates/logout/',
            '/candidates/instructions/GT/',
            '/candidates/instructions/TT/',
            '/candidates/dashboard/',
            '/email_scheduler/export-exam-summary/',
            '/email_scheduler/export-tests-excel/',
            '/'
        ]
        test_page_pattern = re.compile(r'^/exam_dashboard/(test_page|technical_test_page)/\d+/$')
        if not request.session.get('user_id') or request.path in excluded_paths:
            return self.get_response(request)

        try:
            user = Users.objects.get(user_id=request.session.get('user_id'), is_active=True, deleted=False)
            user_invite = UserInvite.objects.filter(user=user, is_mail_sent=True).order_by('-invitation_date').first()
            
            if not user_invite or not user_invite.date_of_exam or not user_invite.start_time_slot:
                messages.error(request, "No valid exam schedule found. Please contact support.")
                request.session.flush()
                logger.error(f"Session expired: No valid UserInvite for user ID {user.user_id}.")
                return redirect('user_login')

            login_window_minutes = self.get_config_value('login_window_duration', 30, int)
            try:
                start_datetime = datetime.combine(user_invite.date_of_exam, user_invite.start_time_slot)
            except TypeError as e:
                logger.error(f"Invalid date/time format for user {user.email}: date_of_exam={user_invite.date_of_exam}, start_time_slot={user_invite.start_time_slot}, error={str(e)}")
                messages.error(request, "Invalid exam schedule data. Please contact support.")
                request.session.flush()
                return redirect('user_login')

            end_datetime = start_datetime + timedelta(minutes=login_window_minutes)
            current_datetime = timezone.now()

            # Restrict test pages to time window
            if request.path.startswith('/start-exam/') or test_page_pattern.match(request.path):
                if not (start_datetime <= current_datetime <= end_datetime):
                    messages.error(request, f"You can only access the test between {start_datetime.strftime('%I:%M %p')} and {end_datetime.strftime('%I:%M %p')} on {user_invite.date_of_exam.strftime('%Y-%m-%d')}.")
                    logger.info(f"Access denied for {user.email} (ID: {user.user_id}) at {current_datetime}: Exam time slot ended at {end_datetime}.")
                    return redirect('test_selection')

            request.session['exam_end'] = end_datetime.isoformat()

        except Users.DoesNotExist:
            messages.error(request, "User not found or account is inactive.")
            request.session.flush()
            logger.error(f"Session expired: User ID {request.session.get('user_id')} not found or inactive.")
            return redirect('user_login')
        except Exception as e:
            messages.error(request, "An error occurred. Please contact support.")
            request.session.flush()
            logger.error(f"Error in middleware for user ID {request.session.get('user_id')}: {str(e)}")
            return redirect('user_login')

        return self.get_response(request)

    def get_config_value(self, key, default=None, cast_type=None):
        try:
            config = Configuration.objects.get(key=key, deleted=False)
            value = config.value
            if cast_type:
                return cast_type(value)
            return value
        except Configuration.DoesNotExist:
            logger.error(f"Configuration key {key} not found.")
            return default
        except Exception as e:
            logger.error(f"Error retrieving config {key}: {str(e)}")
            return default