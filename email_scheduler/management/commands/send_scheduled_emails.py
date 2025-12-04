from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from home.users.models import Users, Configuration  # Import from home.users app
import logging
import time
import socket
from datetime import datetime
from smtplib import SMTPException, SMTPRecipientsRefused
import re

logger = logging.getLogger(__name__)

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class Command(BaseCommand):
    help = 'Send scheduled emails to users in batches'

    def handle(self, *args, **kwargs):
        current_year = str(timezone.now().year)
        config_keys = [
            f'contact_numbers_{current_year}',
            f'recruitment_drive_dates_{current_year}'
        ]
        config = {c.key: c.value for c in Configuration.objects.filter(key__in=config_keys)}
        
        # Debug: Check total users
        total_users = Users.objects.count()
        self.stdout.write(f"Total users in database: {total_users}")
        
        # Set cutoff to today at 2:00 PM IST
        today = datetime.strptime("29/07/2025", "%d/%m/%Y").date()
        cutoff_time = timezone.make_aware(datetime.combine(today, datetime.strptime("14:00", "%H:%M").time()))
        self.stdout.write(f"Cutoff time: {cutoff_time} (2:00 PM IST)")
        
        # Filter users: registered on or before 2:00 PM IST today
        users = Users.objects.filter(
            sh_mail_status=False,
            registered_at__lte=cutoff_time,
            is_active=True,
            deleted=False
        ).order_by('registered_at')[:400]
        total_filtered = users.count()

        batch_size = 20
        self.stdout.write(f"Processing {total_filtered} users in batches of {batch_size}")

        for i in range(0, total_filtered, batch_size):
            batch = users[i:i + batch_size]
            emails = []
            user_ids = []
            failed_user_ids = []

            for user in batch:
                self.stdout.write(f"Preparing email for user {user.user_id}: {user.email}")
                # Check if email is valid
                if not re.match(EMAIL_REGEX, user.email):
                    self.stdout.write(f"❌ Invalid email format: {user.email}")
                    logger.warning(f"Invalid email format: {user.email}")
                    Users.objects.filter(user_id=user.user_id).update(is_email_valid=False)
                    failed_user_ids.append(user.user_id)
                    continue  # Skip sending email

                subject = f"Update for Freshers Recruitment Drive - {current_year}"
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [user.email]

                context = {
                    'first_name': user.first_name,
                    'registration_id': user.registration_id,
                    'config': {
                        'contact_numbers': config.get(f'contact_numbers_{current_year}'),
                        'recruitment_drive_dates': config.get(f'recruitment_drive_dates_{current_year}')
                    }
                }

                html_content = render_to_string('emails/scheduled_notification.html', context)
                text_content = ''

                msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                msg.attach_alternative(html_content, "text/html")
                emails.append((msg, user.user_id))
                user_ids.append(user.user_id)

            try:
                connection = None
                for msg, uid in emails:
                    if connection:
                        msg.connection = connection
                    else:
                        connection = msg.connection
                    try:
                        msg.send()
                        time.sleep(1)
                        self.stdout.write(f"Email sent to {msg.to[0]}")
                    except SMTPRecipientsRefused as e:
                        self.stdout.write(f"❌ Invalid email address: {msg.to[0]}")
                        logger.warning(f"Invalid recipient: {msg.to[0]} — {str(e)}")
                        failed_user_ids.append(uid)
                    except SMTPException as e:
                        self.stdout.write(f"❌ SMTP Error for: {msg.to[0]}")
                        logger.error(f"SMTP error for {msg.to[0]}: {str(e)}")
                        failed_user_ids.append(uid)
                    except socket.error as e:
                        self.stdout.write(f"❌ Network error while sending to {msg.to[0]}")
                        logger.error(f"Socket error for {msg.to[0]}: {str(e)}")
                        failed_user_ids.append(uid)
                    except Exception as e:
                        self.stdout.write(f"❌ Unexpected error for {msg.to[0]}")
                        logger.exception(f"Unexpected error for {msg.to[0]}: {str(e)}")
                        failed_user_ids.append(uid)
                # Only update sh_mail_status for users whose emails were sent successfully
                successful_user_ids = [uid for uid in user_ids if uid not in failed_user_ids]
                if successful_user_ids:
                    Users.objects.filter(user_id__in=successful_user_ids).update(sh_mail_status=True)
                    logger.info(f"Sent batch {i//batch_size + 1}: {len(successful_user_ids)} emails")
                    self.stdout.write(f"Sent batch {i//batch_size + 1}: {len(successful_user_ids)} emails")
                if failed_user_ids:
                    logger.warning(f"Batch {i//batch_size + 1}: Failed to send emails to user_ids: {failed_user_ids}")
                    self.stdout.write(f"Batch {i//batch_size + 1}: Failed to send emails to user_ids: {failed_user_ids}")
                time.sleep(120)
            except Exception as e:
                logger.error(f"Failed to send batch {i//batch_size + 1}: {str(e)}")
                self.stdout.write(f"Failed to send batch {i//batch_size + 1}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"Completed sending emails to {total_filtered} users"))