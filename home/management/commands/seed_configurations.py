from django.core.management.base import BaseCommand
from django.utils import timezone
from home.users.models import Configuration
from config_keys.models import ConfigKeys
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Seeds the configuration table with initial data and configID if not exists'

    def handle(self, *args, **kwargs):
        current_year = datetime.now().year  # Dynamically set the current year (2025)

        # Ensure ConfigKeys entries exist
        if not ConfigKeys.objects.exists():
            self.stdout.write(self.style.ERROR('No ConfigKeys entries found. Please run "seed_config_keys" first.'))
            return

        # Define initial configuration data with keys to map to ConfigKeys
        config_data = [
            {
                'key': f'programming_languages_{current_year}',
                'value': 'Python',
                'created_date': datetime.strptime('2025-06-11 19:31:21.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 19:31:28.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'programming_languages_{current_year}',
                'value': 'PHP',
                'created_date': datetime.strptime('2025-06-11 19:31:21.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 19:31:28.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'programming_languages_{current_year}',
                'value': 'QA',
                'created_date': datetime.strptime('2025-06-11 19:31:21.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 19:31:28.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'programming_languages_{current_year}',
                'value': 'FE(FrontEnd)',
                'created_date': datetime.strptime('2025-06-11 19:31:21.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 19:31:28.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'programming_languages_{current_year}',
                'value': '.Net',
                'created_date': datetime.strptime('2025-06-11 19:31:21.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 19:31:28.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'primary_skills_{current_year}',
                'value': '.Net',
                'created_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'primary_skills_{current_year}',
                'value': 'PHP',
                'created_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'primary_skills_{current_year}',
                'value': 'Python',
                'created_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'primary_skills_{current_year}',
                'value': 'FE(FrontEnd)',
                'created_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'primary_skills_{current_year}',
                'value': 'QA',
                'created_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'primary_skills_{current_year}',
                'value': 'DevOps/Cloud Engineering',
                'created_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'primary_skills_{current_year}',
                'value': 'Mobile Developer (Android/IOS)',
                'created_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'primary_skills_{current_year}',
                'value': 'Cyber Security',
                'created_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'primary_skills_{current_year}',
                'value': 'Others',
                'created_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 16:32:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'gt_easy_questions_{current_year}',
                'value': '6',
                'created_date': datetime.strptime('2025-06-11 19:31:57.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 19:31:57.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'gt_medium_questions_{current_year}',
                'value': '7',
                'created_date': datetime.strptime('2025-06-11 19:31:57.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 19:31:57.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'gt_hard_questions_{current_year}',
                'value': '7',
                'created_date': datetime.strptime('2025-06-11 19:36:57.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 19:36:57.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'gt_total_questions_{current_year}',
                'value': '20',
                'created_date': datetime.strptime('2025-06-11 19:36:57.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 19:36:57.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'gt_duration_minutes_{current_year}',
                'value': '25',
                'created_date': datetime.strptime('2025-06-11 19:54:59.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 19:54:59.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'gt_cutoff_pass_score_{current_year}',
                'value': '15',
                'created_date': datetime.strptime('2025-06-11 20:00:26.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:00:26.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'tt_coding_easy_questions_{current_year}',
                'value': '0',
                'created_date': datetime.strptime('2025-06-11 20:02:32.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:02:32.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'tt_coding_medium_questions_{current_year}',
                'value': '0',
                'created_date': datetime.strptime('2025-06-11 20:04:44.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:04:44.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'tt_coding_hard_questions_{current_year}',
                'value': '0',
                'created_date': datetime.strptime('2025-06-11 20:06:29.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-18 20:06:29.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'tt_total_questions_{current_year}',
                'value': '20',
                'created_date': datetime.strptime('2025-06-11 20:07:25.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:07:25.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'tt_mcq_easy_questions_{current_year}',
                'value': '6',
                'created_date': datetime.strptime('2025-06-11 20:02:32.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:02:32.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'tt_mcq_medium_questions_{current_year}',
                'value': '7',
                'created_date': datetime.strptime('2025-06-11 20:04:44.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:04:44.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'tt_mcq_hard_questions_{current_year}',
                'value': '7',
                'created_date': datetime.strptime('2025-06-11 20:06:29.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-18 20:06:29.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'tt_duration_minutes_{current_year}',
                'value': '35',
                'created_date': datetime.strptime('2025-06-11 20:08:54.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:08:54.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'tt_cutoff_pass_score_{current_year}',
                'value': '15',
                'created_date': datetime.strptime('2025-06-11 20:10:09.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:10:09.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'photo_max_size_kb_{current_year}',
                'value': '200',
                'created_date': datetime.strptime('2025-06-11 20:10:09.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:10:09.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'resume_max_size_mb_{current_year}',
                'value': '1',
                'created_date': datetime.strptime('2025-06-11 20:10:09.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:10:09.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'id_proof_max_size_kb_{current_year}',
                'value': '50',
                'created_date': datetime.strptime('2025-06-11 20:10:09.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:10:09.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'certificate_max_size_mb_{current_year}',
                'value': '1',
                'created_date': datetime.strptime('2025-06-11 20:10:09.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-11 20:10:09.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'date_of_exam_{current_year}',
                'value': '2025-07-23',
                'created_date': datetime.strptime('2025-06-19 22:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-19 22:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'time_of_exam_{current_year}',
                'value': '09:00 AM IST',
                'created_date': datetime.strptime('2025-06-19 22:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-19 22:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'slot_timings_{current_year}',
                'value': 'Slot 1: 09:00 AM - 11:00 AM',
                'created_date': datetime.strptime('2025-06-19 22:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-06-19 22:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'contact_numbers_{current_year}',
                'value': '7842181883 / 9063839747',
                'created_date': datetime.strptime('2025-07-11 19:36:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 19:36:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'recruitment_drive_dates_{current_year}',
                'value': '23rd July and 1st August 2025',
                'created_date': datetime.strptime('2025-07-11 19:36:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-11 19:36:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'email_template_{current_year}',
                'value': 'Call Letter',    
                'created_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'email_template_{current_year}',
                'value': 'Shortlisted',
                'created_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'email_template_{current_year}',
                'value': 'Rejected',
                'created_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {   
                'key': f'suspicious_activity_count',
                'value': '9',
                'created_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,

            },
            {   
                'key': f'login_window_duration',
                'value': '30',
                'created_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,

            },
            {
                'key': f'freeze_Major_popup_timesec',
                'value': '30',
                'created_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),    
                'updated_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,

            },
            {
                'key': f'freeze_Small_popup_timesec',
                'value': '15',  
                'created_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            },
            {
                'key': f'suspicious_activity_majorpopup',
                'value': '3',
                'created_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'updated_date': datetime.strptime('2025-07-18 15:00:00.000000', '%Y-%m-%d %H:%M:%S.%f'),
                'deleted': False,
            }
            
        ]

        added_count = 0
        skipped_count = 0

        for data in config_data:
            # Get the configID from ConfigKeys based on the keys field
            config_key_obj = ConfigKeys.objects.filter(keys=data['key']).first()
            if not config_key_obj:
                self.stdout.write(self.style.WARNING(f"No ConfigKeys entry found for key '{data['key']}'. Skipping."))
                skipped_count += 1
                continue

            data['configID'] = str(config_key_obj.id)


            if data['key'].startswith((f'programming_languages_{current_year}',
                                     f'primary_skills_{current_year}',
                                     f'email_template_{current_year}')):
                if not Configuration.objects.filter(
                    key=data['key'],
                    value=data['value'],
                    deleted=False
                ).exists():
                    Configuration.objects.create(
                        key=data['key'],
                        value=data['value'],
                        created_date=data['created_date'],
                        updated_date=data['updated_date'],
                        deleted=data['deleted'],
                        configID=data['configID'],
                    )
                    added_count +=  1
                    self.stdout.write(self.style.SUCCESS(f"Added {data['key'].split('_')[0]}: {data['value']}"))
                else:
                    skipped_count += 1
                    self.stdout.write(self.style.WARNING(f"{data['key'].split('_')[0]} '{data['value']}' already exists, skipping"))
            else:
                if not Configuration.objects.filter(key=data['key'], deleted=False).exists():
                    Configuration.objects.create(
                        key=data['key'],
                        value=data['value'],
                        created_date=data['created_date'],
                        updated_date=data['updated_date'],
                        deleted=data['deleted'],
                        configID=data['configID'],
                    )
                    added_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Added configuration: {data['key']}"))
                else:
                    skipped_count += 1
                    self.stdout.write(self.style.WARNING(f"Configuration '{data['key']}' already exists, skipping"))

        self.stdout.write(self.style.SUCCESS(
            f'Configuration seeding completed! Added {added_count} new entries, skipped {skipped_count} existing entries.'
        ))
