from home.users.models import Users
from .models import UserInvite
from .models import EmailTemplate
from .forms import EmailTemplateForm
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.utils.timezone import now
import datetime
from datetime import date
from datetime import datetime as dt
import logging
import time
import random
from io import BytesIO
from datetime import datetime
from zipfile import ZipFile
from django.http import HttpResponse
from xhtml2pdf import pisa

# Setup logging
logger = logging.getLogger(__name__)

# user_invite/views.py
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import date, datetime as dt
from .models import Users, UserInvite, EmailTemplate
from django.core.paginator import Paginator

def user_invite_list_view(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status', 'all')
    mail_status_filter = request.GET.get('mail_status', 'all')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    sort_reg_id = request.GET.get('sort_reg_id', None)

    # Get all active email templates
    email_templates = EmailTemplate.objects.filter(is_deleted=False)

    # Default sorting by registered_at in descending order
    users = Users.objects.filter(deleted=False).select_related('userinvite').order_by('-user_id')

    if query:
        users = users.filter(
            Q(mobile__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(registration_id__icontains=query) |
            Q(action_status__icontains=query)
        )

    if status_filter != 'all':
        if status_filter == 'registered':
            users = users.filter(
                Q(userinvite__isnull=True) | Q(userinvite__invited_status='registered')
            )
        else:
            users = users.filter(userinvite__invited_status=status_filter)

    if mail_status_filter != 'all':
        is_sent = mail_status_filter == 'sent'
        if is_sent:
            users = users.filter(userinvite__is_bulk_mail_sent=True)
        else:
            users = users.filter(
                Q(userinvite__isnull=True) | Q(userinvite__is_bulk_mail_sent=False)
            )

    if from_date:
        try:
            from_date_obj = date.fromisoformat(from_date)
            users = users.filter(userinvite__date_of_exam__gte=from_date_obj)
        except ValueError:
            from_date = None
            messages.warning(request, "Invalid 'From Date' format. Please use YYYY-MM-DD.")

    if to_date:
        try:
            to_date_obj = date.fromisoformat(to_date)
            users = users.filter(userinvite__date_of_exam__lte=to_date_obj)
        except ValueError:
            to_date = None
            messages.warning(request, "Invalid 'To Date' format. Please use YYYY-MM-DD.")

    if start_time:
        try:
            start_time_obj = dt.strptime(start_time, '%I:%M %p').time()
            users = users.filter(userinvite__start_time_slot__gte=start_time_obj)
        except ValueError:
            start_time = None
            messages.warning(request, "Invalid 'Start Time' format. Please use HH:MM AM/PM.")

    if end_time:
        try:
            end_time_obj = dt.strptime(end_time, '%I:%M %p').time()
            users = users.filter(userinvite__end_time_slot__lte=end_time_obj)
        except ValueError:
            end_time = None
            messages.warning(request, "Invalid 'End Time' format. Please use HH:MM AM/PM.")

    if sort_reg_id:
        sort_order = 'user_id' if sort_reg_id == 'asc' else '-user_id'
        users = users.order_by(sort_order)
        current_sort = 'asc' if sort_reg_id == 'desc' else 'desc'
    else:
        current_sort = 'desc'

    # Pagination
    paginator = Paginator(users, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate counts
    total_users_count = Users.objects.filter(deleted=False).count()
    templates_sent_count = Users.objects.filter(deleted=False, userinvite__is_bulk_mail_sent=True).count()

    context = {
        'page_obj': page_obj,
        'sort_reg_id': sort_reg_id,
        'current_sort': current_sort,
        'query': query or '',
        'status_filter': status_filter,
        'mail_status_filter': mail_status_filter,
        'from_date': from_date or '',
        'to_date': to_date or '',
        'start_time': start_time or '',
        'end_time': end_time or '',
        'today': date.today(),
        'email_templates': email_templates,
        'total_users_count': total_users_count,
        'templates_sent_count': templates_sent_count,
    }
    return render(request, 'user_invite/user_invite_list.html', context)

from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import Template, Context
from django.conf import settings
from .models import Users, EmailTemplate, Configuration, UserInvite
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import datetime as dt
import logging
import time
from django.db import transaction

logger = logging.getLogger(__name__)
current_year = dt.now().year

def send_bulk_email(request):
    logger.debug("Entering send_bulk_email with method: %s", request.method)
    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return redirect('user_invite_list')

    selected_ids = request.POST.get('selected_users', '').split(',')
    selected_ids = [id.strip() for id in selected_ids if id.strip() and id.strip().isdigit()]
    template_id = request.POST.get('email_template')
    date_of_exam = request.POST.get('date_of_exam')
    start_time_slot = request.POST.get('start_time_slot')
    end_time_slot = request.POST.get('end_time_slot')

    if not selected_ids:
        messages.error(request, "No users selected.")
        return redirect('user_invite_list')

    try:
        email_template = EmailTemplate.objects.get(email_id=template_id, is_deleted=False)
    except EmailTemplate.DoesNotExist:
        messages.error(request, "Invalid email template selected.")
        return redirect('user_invite_list')

    # Check if this is a call letter template
    is_call_letter = "call_letter" in email_template.email_template.lower()

    parsed_date = None
    parsed_start_time = None
    parsed_end_time = None

    if date_of_exam:
        try:
            parsed_date = dt.strptime(date_of_exam, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect('user_invite_list')

    if start_time_slot and end_time_slot:
        try:
            parsed_start_time = dt.strptime(start_time_slot, '%I:%M %p').time()
            parsed_end_time = dt.strptime(end_time_slot, '%I:%M %p').time()
            if parsed_end_time <= parsed_start_time:
                raise ValueError("End time must be after start time.")
        except ValueError as e:
            messages.error(request, f"Invalid time: {str(e)}")
            return redirect('user_invite_list')
    elif start_time_slot or end_time_slot:
        messages.error(request, "Provide both start/end times or neither.")
        return redirect('user_invite_list')

    # Filter active users
    users = Users.objects.filter(
        user_id__in=selected_ids,
        deleted=False
    ).prefetch_related('userinvite')

    batch_size = 20
    total_users = len(users)
    sent_count = 0
    skipped_count = 0

    try:
        with get_connection() as connection:
            for i in range(0, total_users, batch_size):
                batch = users[i:i + batch_size]
                batch_errors = []

                with transaction.atomic():
                    for user in batch:
                        try:
                            # Get or create user invite
                            invite, created = UserInvite.objects.get_or_create(
                                user=user,
                                defaults={
                                    'invited_status': 'invited',
                                    'is_mail_sent': False,
                                    'is_bulk_mail_sent': False,
                                    'date_of_exam': parsed_date,
                                    'start_time_slot': parsed_start_time,
                                    'end_time_slot': parsed_end_time,
                                    'invitation_date': timezone.now(),
                                    'email_template_used': None,
                                    'email_type_sent': None
                                }
                            )

                            # Check if this is a call letter and if one was already sent (successfully)
                            if is_call_letter:
                                # Check if any successful call letter was sent before
                                previous_call_letter_sent = UserInvite.objects.filter(
                                    user=user,
                                    email_type_sent__icontains='call_letter',
                                    is_mail_sent=True
                                ).exists()
                                
                                if previous_call_letter_sent:
                                    logger.info(f"Skipping user {user.email} (ID: {user.user_id}) - call letter already sent")
                                    skipped_count += 1
                                    continue

                            # Check if this specific template has already been sent to the user
                            if invite.email_type_sent == email_template.email_template:
                                logger.info(f"Skipping user {user.email} (ID: {user.user_id}) - template {email_template.email_template} already sent")
                                skipped_count += 1
                                continue

                            # Ensure confirmation_token and URL exist or generate them
                            if not user.confirmation_url or not user.confirmation_token:
                                user.confirmation_token = str(uuid.uuid4())
                                user.confirmation_url = f"https://registration.intelligenzit.com/invite/user/confirmation/{user.registration_id}/{user.confirmation_token}"
                                user.save(update_fields=['confirmation_token', 'confirmation_url'])
                                logger.warning(f"Generated confirmation URL for user {user.email} (ID: {user.user_id}): {user.confirmation_url}")

                            # Prepare context with exam details
                            context = {
                                'user': user,
                                'exam': {
                                    'date': parsed_date.strftime('%dth %B %Y') if parsed_date else '2nd or 3rd August 2025',
                                    'time_slot': start_time_slot if start_time_slot else '9:00 AM'
                                },
                                'venue': {
                                    'company_name': 'Intelligenz IT Info Solutions Pvt Ltd',
                                    'address_line1': '#Plot No 23 & 24, 1st Floor,',
                                    'address_line2': 'Silicon Park, Silicon Valley,',
                                    'address_line3': 'Beside ICICI Bank Lane,',
                                    'address_line4': 'Capitol Park Lane, Madhapur,',
                                    'city': 'Hyderabad',
                                    'pincode': '500 081',
                                    'google_maps_url': 'https://maps.app.goo.gl/3LdsG2g8PSTquPHM8'
                                },
                                'contact': {
                                    'email': 'resumes@intelligenzit.com',
                                    'phone': '7842181883/ 9063839746'
                                },
                                'config': {
                                    'current_year': str(current_year),
                                    'contact_numbers': Configuration.objects.filter(key=f'contact_numbers_{current_year}').first().value if Configuration.objects.filter(key=f'contact_numbers_{current_year}').exists() else 'N/A',
                                    'recruitment_drive_dates': f"{date_of_exam} {start_time_slot} - {end_time_slot}" if parsed_date and parsed_start_time and parsed_end_time else Configuration.objects.filter(key=f'recruitment_drive_dates_{current_year}').first().value if Configuration.objects.filter(key=f'recruitment_drive_dates_{current_year}').exists() else '23rd July 2025 at 09:00 AM'
                                }
                            }

                            try:
                                template_obj = Template(email_template.email_context)
                                html_content = template_obj.render(Context(context))
                                text_content = strip_tags(html_content)
                                logger.debug(f"Rendered HTML for {user.email}: {html_content[:500]}...")
                            except Exception as e:
                                 raise ValueError(f"Template rendering error for {user.email}: {str(e)}")
                            subject = email_template.subject

                            if parsed_date:
                                subject += f" on {parsed_date.strftime('%d-%m-%Y')}"
                            subject = subject.strip()

                            if not subject:
                                raise ValueError("Email subject cannot be empty")

                            msg = EmailMultiAlternatives(
                                subject=subject,
                                body=text_content,
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                to=[user.email],
                                connection=connection
                            )
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()

                            # Update invite with the template used
                            invite.email_template_used = email_template.email_template
                            invite.email_type_sent = email_template.email_template
                            invite.is_mail_sent = True
                            invite.is_bulk_mail_sent = True
                            invite.date_of_exam = parsed_date
                            invite.start_time_slot = parsed_start_time
                            invite.end_time_slot = parsed_end_time
                            invite.save()
                            
                            user.action_status = f"{email_template.email_template}_sent"
                            user.save(update_fields=['action_status'])
                            sent_count += 1

                        except Exception as e:
                            batch_errors.append(f"{user.email}: {str(e)}")
                            user.action_status = f"{email_template.email_template}_failed" if 'email_template' in locals() else f"unknown_template_failed"
                            user.save(update_fields=['action_status'])
                            logger.error(f"Error sending to {user.email}: {str(e)}")

                if batch_errors:
                    messages.error(request, f"Batch errors: {', '.join(batch_errors)}")
                else:
                    messages.info(request, f"Batch {i//batch_size + 1} completed successfully.")

                if i + batch_size < total_users:
                    time.sleep(5)

        if sent_count == total_users:
            messages.success(request, f"All {sent_count} emails sent successfully!")
        else:
            messages.warning(request, f"Sent {sent_count} of {total_users} emails. {skipped_count} users skipped (already received this type of email).")

    except Exception as e:
        logger.error(f"Bulk email failed: {str(e)}")
        messages.error(request, f"Failed to send emails: {str(e)}")

    return redirect('user_invite_list')
def email_template_list(request):
    templates = EmailTemplate.objects.filter(is_deleted=False)
    return render(request, 'email_templates/list.html', {'templates': templates})

def email_template_create(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email template created successfully.')
            return redirect('email_template_list')
    else:
        form = EmailTemplateForm()
    return render(request, 'email_templates/create.html', {'form': form})

def email_template_edit(request, email_id):
    template =OrmTemplate = get_object_or_404(EmailTemplate, pk=email_id)
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email template updated successfully.')
            return redirect('email_template_list')
    else:
        form = EmailTemplateForm(instance=template)
    return render(request, 'email_templates/edit.html', {'form': form, 'template': template})

def email_template_delete(request, email_id):
    template = get_object_or_404(EmailTemplate, pk=email_id)
    template.is_deleted = True
    template.save()
    messages.success(request, 'Email template deleted successfully.')
    return redirect('email_template_list')

def confirm_registration(request, registration_id, confirmation_token):
    logger.debug(f"Querying for registration_id={registration_id}, confirmation_token={confirmation_token}")
    user = get_object_or_404(
        Users,
        registration_id=registration_id,
        confirmation_token=confirmation_token,
        deleted=False
    )
    
    try:
        if user.user_confirmation_status == 1:
            logger.info(f"User {user.email} (ID: {user.user_id}) registration already confirmed")
            messages.info(request, "Your registration is already confirmed.")
        else:
            logger.debug(f"Before save: user_confirmation_status={user.user_confirmation_status}")
            user.user_confirmation_status = 1
            user.save(update_fields=['user_confirmation_status'])
            logger.debug(f"After save: user_confirmation_status={user.user_confirmation_status}")
            logger.info(f"User {user.email} (ID: {user.user_id}) confirmed registration")
            messages.success(request, "Thanks for confirming your registration!")
    except Exception as e:
        logger.error(f"Failed to confirm registration for {user.email}: {str(e)}")
        messages.error(request, "Failed to confirm registration. Please contact support.")
    
    return render(request, 'user_invite/confirmation_success.html', {'user': user})

def download_bulk_pdfs(request):
    if request.method != 'POST':
        return HttpResponse('Invalid request method', status=400)
    
    selected_ids = request.POST.get('selected_users', '').split(',')
    selected_ids = [id.strip() for id in selected_ids if id.strip()]
    
    # Get users - all if none selected
    if selected_ids:
        users = Users.objects.filter(user_id__in=selected_ids, deleted=False)
    else:
        users = Users.objects.filter(deleted=False)
    
    # Create zip file in memory
    zip_buffer = BytesIO()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        with ZipFile(zip_buffer, 'w') as zip_file:
            for user in users:
                try:
                    # Render HTML template with user data
                    context = {
                        'user': user,
                        'invite': user.userinvite if hasattr(user, 'userinvite') else None
                    }
                    html = render_to_string('user_invite/user_pdf_template.html', context)
                    
                    # Create PDF
                    pdf = BytesIO()
                    pisa_status = pisa.CreatePDF(html, dest=pdf)
                    
                    if pisa_status.err:
                        logger.error(f"PDF creation failed for user {user.user_id}")
                        continue
                    
                    # Add to zip
                    zip_file.writestr(f"{user.registration_id}.pdf", pdf.getvalue())
                    
                except Exception as e:
                    logger.error(f"Error generating PDF for user {user.user_id}: {str(e)}")
                    continue
    
        # Prepare the response
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="user_pdfs_{timestamp}.zip"'
        return response
        
    except Exception as e:
        logger.error(f"Bulk PDF generation failed: {str(e)}")
        return HttpResponse(f"Error generating PDFs: {str(e)}", status=500)

