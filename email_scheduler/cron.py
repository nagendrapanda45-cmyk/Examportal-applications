from django_cron import CronJobBase, Schedule
from django.core.management import call_command
import traceback

print(">>> Loading email_scheduler.cron module...")

class SendScheduledEmailsCronJob(CronJobBase):
    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'email_scheduler.send_scheduled_emails'

    def do(self):
        print(">>> Inside do() method")
        try:
            call_command('send_scheduled_emails')
        except Exception as e:
            print("❌ Error in cron job:")
            traceback.print_exc()
