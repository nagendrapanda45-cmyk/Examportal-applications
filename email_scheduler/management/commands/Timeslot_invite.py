from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from home.users.models import Users
from user_invite.models import UserInvite
import logging
import time
import socket
from smtplib import SMTPException, SMTPRecipientsRefused
from datetime import date, datetime, timedelta
from Exam_dashboard.views import assign_test_questions,get_config_value,bulk_create_test_answers
from home.users.models import Tests, TestUserQuestionAnswer,Question



logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Send exam invitations in time slots to users"

    def handle(self, *args, **kwargs):
        # ✅ Exam date is set here
        # exam_date = date(2025, 9, 22)   # YYYY, MM, DD) 
        exam_date = date.today() + timedelta(days=1)
        yesterday = date.today() - timedelta(days=20)
        formatted_yesterday = yesterday.strftime("%Y-%m-%d")

        current_year = timezone.now().year
 
 
 
        # Clean up un-submitted tests from the previous day
 
        # unsubmitted_tests = Tests.objects.filter(
        #     created_at__date__lte=formatted_yesterday,
        #     is_submitted=False,
        #     test_status=0
        # )
        # deleted_test_count = unsubmitted_tests.count()
        # if deleted_test_count > 0:
        #     # Delete associated TestUserQuestionAnswer records
        #     deleted_answer_count = TestUserQuestionAnswer.objects.filter(
        #         test__in=unsubmitted_tests
        #     ).delete()
        #     # Delete Tests records
        #     unsubmitted_tests.delete()
        #     self.stdout.write(f"🗑️ Deleted {deleted_test_count} un-submitted tests and {deleted_answer_count} TestUserQuestionAnswer records from {yesterday}.")
        # else:
        #     self.stdout.write(f"✅ No un-submitted tests from {yesterday} to delete.")

        # ✅ Fetch users who haven't been invited
        users = Users.objects.filter(
            invite_mail_status=False,
            is_active=True,
            deleted=False
            # ,
            # email__in=['naresh@altnsolutions.co.uk']
            # email__in=['naresh@altnsolutions.co.uk','dronavalli579@gmail.com','janilsrg@gmail.com','ibrahimshaik7787@gmail.com','chandniaich23@gmail.com','nsangeeta2002@gmail.com','ravi.kandakatla@gmail.com']
        ).order_by('user_id')[:2500]
        # .exclude(
        #     user_id__in=[10439,10578,10461,10406,10312,10512,10319,10456,10473,10537,10654,10418,10523,10463,10621,10705,11231,10976,11031,11096,10931,11134,11114,11145,11298,10899,10883,11200,11269,11781,11478,11445,11453,11757,11610,11599,11634,11516,11461,11745,11676,11420,11381,11654,11448,11750,11356,11595,11696,11497,11624,11680,11677,11472,11759,11719,11756,11391,11722,11515,11347,11346,11401,11633,11537,11665,11466,11716,11372,11657,11480,11489,11343,11785,11594,11534,11701,11366,11775,11670,11580,11455,11720,11575,11336,11751,11501,11674,11425,11571,11664,11609,11572,11521,11898,11804,11806,12258,12260,11833,11981,11923,12177,12051,11999,12008,12094,12259,12163,11850,11911,11810,12137,12038,11966,11811,11918,11894,12230,11908,12139,12277,11953,11948,12142,11900,12266,11893,12054,12197,12185,11905,12088,12069,11969,11849,12035,11902,11858,11982,12224,12263,12131,11906,12273,11954,12293,11878,12151,11824,11840,11843,12192,12193,12130,12278,10301,11807,12004,12065,11814,12050,11690,11319,11369,11593,11456,11528,11394,11500,11432,11442,11512,11405,11339,11546,11503,11644,11376,11672,11741,11792,11642,11465,11623,11354,11441,11450,11467,11344,11494,11353,11352,11684,11439,11464,11484,11766,11533,11600,11603,11662,11498,11327,11704,11660,11620,11771,11544,11776,11592,11649,11387,11556,11374,11416,11596,11638,11424,11452,11302,11794,11627,11797,11692,11737,11723,11631,11385,11782,11621,11673,11647,11688,11483,11744,11706,11433,11761,11584,11334,11788,11753,11643,11579,11645,11355,11557,11539,11322,11778,11748,11614,11697,11590,11625,11462,11641,11668,11380,11698,11795,11504,11430,11409,11749,11437,11612,11727,11586,11679,11746,11431,11768,11760,11587,11777,11378,11648,11801,11509,11656,11330,10805,11078,11139,10838,10887,11241,10971,11194,10873,11293,11162,11189,11125,11214,11198,10881,10949,11146,10963,11258,11210,10935,11209,10814,10894,11017,11230,11192,10849,10901,11083,10928,10812,10877,10817,10910,11295,11169,11299,11154,10701,10331,10459,10494,10444,10688,10525,10396,10380,10415,10603,10649,10407,10801,10458,10464,10403,10532,10352,10550,10638,10787,10673,10642,10334,10498,10371,10568,10302,10796,10572,10402,10553,10765,10375,10686,10535,10735,10509]
        # )

        if not users.exists():
            self.stdout.write("✅ No users pending for invitations.")
            return

        # ✅ Prepare time slots
        time_slots = [
            # ("09:00", "10:30"),
            # ("11:00", "12:30"),
            # ("13:00", "14:30"),
            # ("15:00", "16:30"),
            ("17:00", "18:30"),
        ]

        users_per_slot = 500
        total_users = users.count()
        self.stdout.write(f"📩 Total pending users: {total_users}")

        slot_index = 0
        batch = 0

        for i, user in enumerate(users, start=1):
            # pick current slot
            start_time, end_time = time_slots[slot_index]

            subject = "Freshers’ Drive Test – Employee Communication"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            # Convert start and end times to 12-hour format with AM/PM
            start_time_12hr = datetime.strptime(start_time, "%H:%M").strftime("%I:%M %p")
            end_time_12hr = datetime.strptime(end_time, "%H:%M").strftime("%I:%M %p")
            context = {
                "first_name": user.first_name,
                "user": user,
                "exam_date": exam_date.strftime("%d %B %Y"),  # e.g., "03 September 2025"
                "start_time": start_time_12hr,
                "end_time": end_time_12hr,
                "registration_id": user.registration_id,
                "dob": user.dob.strftime("%d/%m/%Y") if user.dob else "",
            }

            html_content = render_to_string("emails/Timeslot_Invite_mail.html", context)

            msg = EmailMultiAlternatives(subject, "", from_email, to_email)
            msg.attach_alternative(html_content, "text/html")

            try:
                msg.send()
                time.sleep(1)  # throttle sending
                self.stdout.write(f"✅ Email sent to {user.email} (Slot {start_time}-{end_time})")

                # Create UserInvite record
                user_invite,created=UserInvite.objects.update_or_create(
                    user=user,
                    defaults={
                        "invited_status": "invited",
                        "invitation_date": timezone.now(),
                        "date_of_exam": exam_date,
                        "start_time_slot": start_time,
                        "end_time_slot": end_time,
                        "is_mail_sent": True,
                        "email_template_used": "emails/Timeslot_Invite_mail.html",
                        "email_type_sent": "invitation_letter",
                    },
                )

                # ✅ Update user status
                user.invite_mail_status = True
                user.invite_email_exception = None
                user.save(update_fields=["invite_mail_status", "invite_email_exception"])
                result = assign_test_questions(user.user_id)
                if not result.get('success'):
                    self.stdout.write(f"❌ Error pre-assigning GT questions to {user.email}: {result['error']}")
                    logger.error(f"Error pre-assigning GT questions to {user.email}: {result['error']}")
                    # continue
                self.stdout.write(f"✅ GT questions pre-assigned to {user.email}: {result['message']}")

            except (SMTPRecipientsRefused, SMTPException, socket.error, Exception) as e:
                error_message = str(e)
                self.stdout.write(f"❌ Error sending email to {user.email}: {error_message}")
                logger.exception(f"Error sending email to {user.email}: {error_message}")

                # ✅ Store exception in Users table
                user.invite_mail_status = False
                user.invite_email_exception = error_message
                user.save(update_fields=["invite_mail_status", "invite_email_exception"])

            # ✅ Move to next slot every 100 users
            if i % users_per_slot == 0:
                slot_index = (slot_index + 1) % len(time_slots)
                batch += 1
                self.stdout.write(f"⏭️ Moved to next slot ({slot_index}) after batch {batch}")

        self.stdout.write("🎯 Invitation process completed.")
