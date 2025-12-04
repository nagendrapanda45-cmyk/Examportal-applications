from django.core.management.base import BaseCommand
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from user_invite.models import UserInvite
from datetime import datetime, timedelta, time

# 🔑 Outlook SMTP Credentials (set your details here)
OUTLOOK_EMAIL = "registrations1@techraq.com"
OUTLOOK_APP_PASSWORD = "byvldghkkbcmdmdh"

class Command(BaseCommand):
    help = "Send reminder emails to users 1 hour before their exam slot"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        today = now.date()
        current_time = now.time()

        # 📌 Fetch invites
        invites = UserInvite.objects.filter(
            date_of_exam=today,
            slot_remainder_mail=False,
            is_deleted=False
        )

        if not invites.exists():
            self.stdout.write("✅ No reminder mails to send.")
            return

        sent_count = 0
        skipped_count = 0
        batch_number = 0

        # 🔗 Outlook SMTP connection
        connection = get_connection(
            host="smtp.office365.com",
            port=587,
            username=OUTLOOK_EMAIL,
            password=OUTLOOK_APP_PASSWORD,
            use_tls=True,
        )

        batch = []
        for invite in invites:
            slot_start_time = invite.start_time_slot
            
            # Calculate the reminder time (4 hour before exam slot)
            reminder_time = self.subtract_time(slot_start_time, hours=6)
            
            # ✅ strict 1-hour condition using time comparison
            if reminder_time <= current_time < slot_start_time:
                batch.append(invite)

                if len(batch) == 20:
                    batch_number += 1
                    self.stdout.write(f"\n📦 Preparing Batch {batch_number} with {len(batch)} users...")
                    sent_in_batch, failed_in_batch = self.send_batch(batch, connection, batch_number)
                    sent_count += sent_in_batch
                    skipped_count += failed_in_batch
                    self.stdout.write(f"✅ Batch {batch_number} completed: {sent_in_batch} sent, {failed_in_batch} failed\n")
                    batch = []
            else:
                skipped_count += 1

        # last batch if remaining
        if batch:
            batch_number += 1
            self.stdout.write(f"\n📦 Preparing Batch {batch_number} with {len(batch)} users...")
            sent_in_batch, failed_in_batch = self.send_batch(batch, connection, batch_number)
            sent_count += sent_in_batch
            skipped_count += failed_in_batch
            self.stdout.write(f"✅ Batch {batch_number} completed: {sent_in_batch} sent, {failed_in_batch} failed\n")

        # 🔹 Final summary
        self.stdout.write("📊 ===== FINAL SUMMARY =====")
        self.stdout.write(f"📩 Total reminder mails sent: {sent_count}")
        self.stdout.write(f"⏭️ Total skipped/failed: {skipped_count}")
        self.stdout.write("🎯 Reminder process finished.")

    def subtract_time(self, time_obj, hours=0, minutes=0):
        """Subtract hours/minutes from a time object and return a time object"""
        total_minutes = time_obj.hour * 60 + time_obj.minute - hours * 60 - minutes
        total_minutes %= 1440  # Ensure it stays within 24 hours
        
        new_hour = total_minutes // 60
        new_minute = total_minutes % 60
        
        return time(new_hour, new_minute)

    def send_batch(self, batch, connection, batch_number):
        sent = 0
        failed = 0

        for i, invite in enumerate(batch, start=1):
            subject = "Reminder: Upcoming Fresher Drive Test"
            to_email = [invite.user.email]

            context = {
                "first_name": invite.user.first_name,
                "exam_date": invite.date_of_exam.strftime("%d %B %Y"),
                "start_time": invite.start_time_slot.strftime("%I:%M %p"),
                "end_time": invite.end_time_slot.strftime("%I:%M %p"),
                "registration_id": invite.user.registration_id,
                "dob": invite.user.dob.strftime("%d/%m/%Y") if invite.user.dob else "",
            }

            html_content = render_to_string("emails/Slot_remainder_mail.html", context)

            msg = EmailMultiAlternatives(
                subject,
                "",  # no plain text
                OUTLOOK_EMAIL,
                to_email,
                connection=connection
            )
            msg.attach_alternative(html_content, "text/html")

            self.stdout.write(f"   📧 Preparing mail {i}/{len(batch)} for {to_email[0]}...")

            try:
                msg.send()
                sent += 1
                invite.slot_remainder_mail = True
                invite.save(update_fields=["slot_remainder_mail"])
                self.stdout.write(f"      ✅ Sent to {to_email[0]}")
            except Exception as e:
                failed += 1
                self.stdout.write(f"      ❌ Failed for {to_email[0]}: {str(e)}")

        return sent, failed