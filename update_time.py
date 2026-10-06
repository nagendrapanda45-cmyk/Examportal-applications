import os, django, datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from user_invite.models import UserInvite

invites = UserInvite.objects.all()
if invites.exists():
    invite = invites.last()
    now = datetime.datetime.now()
    invite.start_time_slot = (now - datetime.timedelta(minutes=5)).time()
    invite.end_time_slot = (now + datetime.timedelta(minutes=55)).time()
    invite.save()
    print(f"Updated invite time to {invite.start_time_slot.strftime('%I:%M %p')} - {invite.end_time_slot.strftime('%I:%M %p')}")
else:
    print("No invites found!")
