from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Users
from .forms import UsersForm
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import UserRegistrationForm, UserLoginForm
from .models import Users, Instruction, Tests,Configuration
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Image
from django.conf import settings
from reportlab.lib import colors
import io
import os
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging
from user_invite.models import UserInvite
from django.urls import reverse
from datetime import datetime,timedelta
import requests
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.contrib.sessions.models import Session
logger = logging.getLogger(__name__)
current_year = datetime.now().year
def get_config_value(key, default=None, cast_type=None):
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
@login_required
def user_list_view(request):
    query = request.GET.get('q')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    users = Users.objects.filter(deleted=False).order_by('-user_id')
    
    # # Generate confirmation tokens for users without tokens and pending status
    # for user in users.filter(confirmation_token__isnull=True, user_confirmation_status=0):
    #     try:
    #         if not user.user_id or not user.email:
    #             logger.warning(f"Skipping token generation for user {user.id}: Missing user_id or email")
    #             continue
    #         user.confirmation_token = user.generate_confirmation_token()
    #         user.save(update_fields=['confirmation_token'])
    #         logger.info(f"Generated confirmation token for user {user.email}: {user.confirmation_token}")
    #     except Exception as e:
    #         logger.error(f"Failed to generate confirmation token for user {user.email}: {str(e)}")

    if query:
        users = users.filter(
            Q(mobile__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(registration_id__icontains=query)
        )
    
    if from_date:
        try:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
            users = users.filter(registered_at__gte=from_date_obj)
        except ValueError:
            from_date = None
            pass
    
    if to_date:
        try:
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')
            to_date_obj = to_date_obj.replace(hour=23, minute=59, second=59)
            users = users.filter(registered_at__lte=to_date_obj)
        except ValueError:
            to_date = None
            pass
    
    # Pagination
    paginator = Paginator(users, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user_list.html', {
        'page_obj': page_obj,
        'from_date': from_date,
        'to_date': to_date
    })

@login_required
def user_create_view(request):
    config_keys = [
        f'photo_max_size_kb_{current_year}', f'resume_max_size_mb_{current_year}',
        f'id_proof_max_size_kb_{current_year}', f'certificate_max_size_mb_{current_year}',
        'current_year', f'contact_numbers_{current_year}', f'recruitment_drive_dates_{current_year}'
    ]
    config = {c.key: c.value for c in Configuration.objects.filter(key__in=config_keys)}
    
    if request.method == 'POST':
        form = UsersForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # FIX: Explicitly set the action_status to 'registered' for admin-created users
            user.action_status = 'registered'
            user.save()
            
            year = config.get(str(datetime.now().year))
            dob_str = user.dob.strftime("%Y%m%d")
            user.registration_id = f"REG-{year}-{dob_str}-{user.user_id}"
            user.save(update_fields=['registration_id'])

            # Send registration email
            subject = f"Registration Confirmation - Freshers Drive {year}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            context = {
                'first_name': user.first_name,
                'registration_id': user.registration_id,
                'config': {
                    'current_year': str(datetime.now().year),
                    'contact_numbers': config.get(f'contact_numbers_{current_year}' ),
                    'recruitment_drive_dates': config.get(f'recruitment_drive_dates_{current_year}')
                }
            }
            text_content = render_to_string('emails/registration_confirmation.txt', context)
            html_content = render_to_string('emails/registration_confirmation.html', context)

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
                print("Email sent successfully.")
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
                messages.warning(request, 'User created but email failed to send.')

            messages.success(request, 'User registered successfully and email sent.')
            return redirect('user_list')
        # The 'else' block below is where the change is.
        # I have removed the generic error message to prevent the popup.
        # The form will now display specific errors next to each field.
        else:
            pass # No generic error message needed. Errors will show on the form.
    else:
        form = UsersForm()

    context = {
        'form': form,
        'photo_size_kb': int(config.get(f'photo_max_size_kb_{current_year}', 1024)),
        'resume_size_mb': round(int(config.get(f'resume_max_size_mb_{current_year}', 5))),
        'id_proof_size_kb': int(config.get(f'id_proof_max_size_kb_{current_year}', 1024)),
        'certificate_size_mb': round(int(config.get(f'certificate_max_size_mb_{current_year}', 5))),
    }
    return render(request, 'user_form.html', context)

@login_required
def user_edit_view(request, pk):
    user = get_object_or_404(Users, pk=pk)
    config_keys = [
        f'photo_max_size_kb_{current_year}', f'resume_max_size_mb_{current_year}',
        f'id_proof_max_size_kb_{current_year}', f'certificate_max_size_mb_{current_year}'
    ]
    config = {c.key: c.value for c in Configuration.objects.filter(key__in=config_keys)}
    
    if request.method == 'POST':
        form = UsersForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UsersForm(instance=user)
    
    context = {
        'form': form,
        'photo_size_kb': int(config.get(f'photo_max_size_kb_{current_year}')),
        'resume_size_mb': round(int(config.get(f'resume_max_size_mb_{current_year}'))),
        'id_proof_size_kb': int(config.get(f'id_proof_max_size_kb_{current_year}')),
        'certificate_size_mb': round(int(config.get(f'certificate_max_size_mb_{current_year}'))),
    }
    return render(request, 'user_form.html', context)

# ... (rest of the views.py file remains unchanged)
# The rest of your code from views.py is correct, so I am omitting it for brevity.
# I will just paste the functions that were present in your original code.
@login_required
def user_delete_view(request, pk):
    user = get_object_or_404(Users, pk=pk)
    user.deleted = True
    user.save()
    return redirect('user_list')
@login_required
def user_pdf_view(request, pk):
    user = get_object_or_404(Users, pk=pk)
    
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Define margins and starting position
    left_margin = inch
    right_margin = width - inch
    top_margin = height - inch
    y = top_margin
    
    # Helper function to check for page break
    def check_page_break(current_y, required_space=0.5 * inch):
        nonlocal y, p
        if current_y < inch + required_space:
            p.showPage()
            y = top_margin
            p.setFont("Helvetica", 12)
        return y
    
    # Helper function to draw section header
    def draw_section_header(title, icon_text="", is_subsection=False):
        nonlocal y
        y = check_page_break(y, 0.7 * inch)
        p.setFont("Helvetica-Bold", 14 if not is_subsection else 12)
        p.setFillColor(colors.darkblue)
        p.drawString(left_margin + (0.2 * inch if is_subsection else 0), y, f"{icon_text}{title}")
        y -= 0.1 * inch
        p.line(left_margin + (0.2 * inch if is_subsection else 0), y, right_margin, y)
        y -= 0.3 * inch
        p.setFont("Helvetica", 12)
        p.setFillColor(colors.black)
    
    # Helper function to wrap text if too long
    def draw_wrapped_text(label, value, x, y, max_width):
        text_object = p.beginText(x, y)
        text_object.setFont("Helvetica", 12)
        # Truncate or wrap long text
        if p.stringWidth(f"{label}: {value}", "Helvetica", 12) > max_width:
            text_object.textLines(f"{label}: {value}", wrapon=True, size=max_width)
        else:
            text_object.textLine(f"{label}: {value}")
        p.drawText(text_object)
        return text_object.getY()
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(left_margin, y, f"Candidate Details:")
    y -= 0.3 * inch
    p.line(left_margin, y, right_margin, y)
    y -= 0.3 * inch
    p.setFont("Helvetica", 12)
    
    # Personal Information Section
    draw_section_header("Personal Information")
    col1_x = left_margin
    col2_x = width / 2
    fields = [
        ("First Name", user.first_name),
        ("Last Name", user.last_name),
        ("Gender", user.gender),
        ("Date of Birth", str(user.dob) if user.dob else "N/A"),
        ("Aadhar Number", user.aadhar_number),
    ]
    for i, (label, value) in enumerate(fields):
        y = check_page_break(y, 0.3 * inch)
        x = col1_x if i % 2 == 0 else col2_x
        p.drawString(x, y, f"{label}: {value}")
        if i % 2 == 1 or i == len(fields) - 1:
            y -= 0.3 * inch
    

    # Contact Information Section
    draw_section_header("Contact Information")
    fields = [
        ("Email", user.email),
        ("Mobile", user.mobile),
        ("Alternative Mobile", user.alternative_mobile or "N/A"),
    ]
    for i, (label, value) in enumerate(fields):
        y = check_page_break(y, 0.3 * inch)
        x = col1_x if i % 2 == 0 else col2_x
        p.drawString(x, y, f"{label}: {value}")
        if i % 2 == 1 or i == len(fields) - 1:
            y -= 0.3 * inch
    
    # Address Details Subsection
    draw_section_header("Address Details", is_subsection=True)
    # Address on a single line (or wrapped)
    y = check_page_break(y, 0.6 * inch)
    y = draw_wrapped_text("Address", user.address, col1_x, y, right_margin - col1_x)
    y -= 0.1 * inch
    # City and Pincode on the next line, side by side
    y = check_page_break(y, 0.3 * inch)
    p.drawString(col1_x, y, f"City: {user.city}")
    p.drawString(col2_x, y, f"Pincode: {user.pincode or 'N/A'}")
    y -= 0.3 * inch
    
    # Educational Information Section
    draw_section_header("Educational Information")
    fields = [
        ("Highest Qualification", user.highest_qualification),
        ("Specific Qualification", user.specific_qualification),
        ("Stream", user.stream or "N/A"),
        ("College/University", user.college_or_university),
        ("Percentage", str(user.highest_qualification_percentage) if user.highest_qualification_percentage else "N/A"),
    ]
    for i, (label, value) in enumerate(fields):
        y = check_page_break(y, 0.6 * inch)
        # Display each field on a new line to prevent mixing
        y = draw_wrapped_text(label, value, col1_x, y, right_margin - col1_x)
        y -= 0.1 * inch
    
    # Skills Subsection
    draw_section_header("Skills", is_subsection=True)
    y = check_page_break(y, 0.6 * inch)
    y = draw_wrapped_text("Primary Skills", user.primary_skills or "N/A", col1_x, y, right_margin - col1_x)
    y -= 0.1 * inch
    
    # Documents Subsection
    draw_section_header("Documents", is_subsection=True)
    img_width = 1.0 * inch
    img_height = 1.0 * inch
    sig_height = 1.0 * inch
    img_spacing = 1.0 * inch
    
    y = check_page_break(y, img_height + 0.4 * inch)
    if user.photo and os.path.exists(os.path.join(settings.MEDIA_ROOT, user.photo.name)):
        try:
            p.drawImage(os.path.join(settings.MEDIA_ROOT, user.photo.name), left_margin, y - img_height, width=img_width, height=img_height, preserveAspectRatio=True)
            p.setFont("Helvetica", 10)
            p.drawString(left_margin, y - img_height - 0.2 * inch, "Profile Photo")
            p.setFont("Helvetica", 12)
        except Exception as e:
            p.drawString(left_margin, y - img_height - 0.2 * inch, f"Error loading photo: {str(e)}")
    else:
        p.drawString(left_margin, y - img_height - 0.2 * inch, "No Profile Photo Available")
    
    sig_x = left_margin + img_width + img_spacing
    # if user.signature and os.path.exists(os.path.join(settings.MEDIA_ROOT, user.signature.name)):
    #     try:
    #         p.drawImage(os.path.join(settings.MEDIA_ROOT, user.signature.name), sig_x, y - img_height, width=img_width, height=sig_height, preserveAspectRatio=True)
    #         p.setFont("Helvetica", 10)
    #         p.drawString(sig_x, y - img_height - 0.2 * inch, "Signature")
    #         p.setFont("Helvetica", 12)
    #     except Exception as e:
    #         p.drawString(sig_x, y - img_height - 0.2 * inch, f"Error loading signature: {str(e)}")
    # else:
    #     p.drawString(sig_x, y - img_height - 0.2 * inch, "No Signature Available")
    
    y -= (img_height + 0.4 * inch)
    
    # Reference Information Section
    draw_section_header("Reference Information")
    fields = [
        ("Reference", user.reference),
        ("Referred By", user.referred_by or "N/A"),
    ]
    for i, (label, value) in enumerate(fields):
        y = check_page_break(y, 0.3 * inch)
        x = col1_x if i % 2 == 0 else col2_x
        p.drawString(x, y, f"{label}: {value}")
        if i % 2 == 1 or i == len(fields) - 1:
            y -= 0.3 * inch
    
    # Additional Information Section
    draw_section_header("Additional Information")
    fields = [
        ("Registration ID", user.registration_id),
        ("Registered At", user.registered_at.strftime('%Y-%m-%d %H:%M:%S')),
    ]
    for label, value in fields:
        y = check_page_break(y, 0.3 * inch)
        p.drawString(col1_x, y, f"{label}: {value}")
        y -= 0.3 * inch
    
    # Finalize PDF
    p.showPage()
    p.save()
    
    # Get PDF from buffer
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="candidate_{user.registration_id}.pdf"'
    response.write(pdf)
    
    return response

#Geetha views# views.py

@csrf_protect
def user_register(request):
    current_year = str(datetime.now().year)
    config_keys = [
        f'photo_max_size_kb_{current_year}', f'resume_max_size_mb_{current_year}',
        f'id_proof_max_size_kb_{current_year}', f'certificate_max_size_mb_{current_year}',
        'current_year', f'contact_numbers_{current_year}', f'recruitment_drive_dates_{current_year}'
    ]
    config = {c.key: c.value for c in Configuration.objects.filter(key__in=config_keys)}

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)

        # RECAPTCHA VALIDATION
        recaptcha_response = request.POST.get('g-recaptcha-response')
        recaptcha_verify = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
        )
        recaptcha_result = recaptcha_verify.json()

        if not recaptcha_result.get('success'):
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return render(request, 'users/register.html', {
                'form': form,
                'photo_size_kb': int(config.get(f'photo_max_size_kb_{current_year}', 1024)),
                'resume_size_mb': round(int(config.get(f'resume_max_size_mb_{current_year}', 5))),
                'id_proof_size_kb': int(config.get(f'id_proof_max_size_kb_{current_year}', 1024)),
                'certificate_size_mb': round(int(config.get(f'certificate_max_size_mb_{current_year}', 5)))
            })

        if form.is_valid():
            user = form.save(commit=False)
            user.action_status = 'pending'  # Set initial action_status
            user.save()  # This will trigger _generate_user_id_and_registration_id and save files

            year = config.get('current_year', str(datetime.now().year))
            dob_str = user.dob.strftime("%Y%m%d")
            user.registration_id = f"REG-{year}-{dob_str}-{user.user_id}"
            user.save(update_fields=['registration_id'])
            
            # Send confirmation email
            subject = f"Registration Confirmation - Freshers Drive {current_year}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            context = {
                'first_name': user.first_name,
                'registration_id': user.registration_id,
                'config': {
                    'current_year': str(datetime.now().year),
                    'contact_numbers': config.get(f'contact_numbers_{current_year}' ),
                    'recruitment_drive_dates': config.get(f'recruitment_drive_dates_{current_year}')
                }
            }
            text_content = render_to_string('emails/registration_confirmation.txt', context)
            html_content = render_to_string('emails/registration_confirmation.html', context)

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
                user.registration_mail_sent = True
                user.action_status = 'registered'  # Update action_status on successful email
                user.save(update_fields=['registration_mail_sent', 'action_status'])
                print("Registration email sent successfully.")
            except Exception as e:
                print(f"Registration email sending failed: {str(e)}")
                messages.warning(request, 'User created but registration email failed to send.')
                user.registration_mail_sent = False
                user.action_status = 'pending'  # Keep status as pending if email fails
                user.save(update_fields=['registration_mail_sent', 'action_status'])
            request.session['registration_id'] = user.registration_id
            return redirect('registration_success')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'photo_size_kb': int(config.get(f'photo_max_size_kb_{current_year}', 1024)),
        'resume_size_mb': round(int(config.get(f'resume_max_size_mb_{current_year}', 5))),
        'id_proof_size_kb': int(config.get(f'id_proof_max_size_kb_{current_year}', 1024)),
        'certificate_size_mb': round(int(config.get(f'certificate_max_size_mb_{current_year}', 5))),
    }

    return render(request, 'users/register.html', context)

def registration_success(request):
    # Retrieve registration_id from session or query parameter
    registration_id = request.session.get('registration_id', 'N/A')
    return render(request, 'users/registration_success.html', {'registration_id': registration_id})

@login_required
def send_exam_details(request, pk):
    user = get_object_or_404(Users, pk=pk)
    current_year = datetime.now().year  # 2025

    # Fetch configuration data
    config = {
        c.key: c.value for c in Configuration.objects.filter(
            key__in=[
                f'date_of_exam_{current_year}',
                f'time_of_exam_{current_year}',
                f'slot_timings_{current_year}',
                f'gt_duration_minutes_{current_year}',
                f'tt_duration_minutes_{current_year}',
                f'contact_number_{current_year}',
                f'gt_total_questions_{current_year}',
                f'tt_total_questions_{current_year}',
                'login_window_duration'
            ]
        )
    }

    # Default values if configuration data is missing
    date_of_exam_str = config.get(f'date_of_exam_{current_year}', '2025-08-25')
    try:
        date_of_exam = datetime.strptime(date_of_exam_str, '%Y-%m-%d').date()
    except ValueError:
        date_of_exam = datetime.now().date()
        logger.error(f"Invalid date_of_exam format: {date_of_exam_str}. Using default: {date_of_exam}")

    slot_timings = config.get(f'slot_timings_{current_year}', '16:00')  # e.g., "16:00"
    try:
        start_time_slot = datetime.strptime(slot_timings, '%H:%M').time()
    except ValueError:
        start_time_slot = time(16, 0)  # Default to 4:00 PM
        logger.error(f"Invalid slot_timings format: {slot_timings}. Using default: {start_time_slot}")

    login_window_minutes = int(config.get('login_window_duration', 10))
    start_datetime = datetime.combine(date_of_exam, start_time_slot)
    end_datetime = start_datetime + timedelta(minutes=login_window_minutes)
    end_time_slot = end_datetime.time()

    # Create or update UserInvite record
    user_invite, created = UserInvite.objects.update_or_create(
        user=user,
        defaults={
            'date_of_exam': date_of_exam,
            'start_time_slot': start_time_slot,
            'end_time_slot': end_time_slot,
            'is_mail_sent': True,
            'invitation_date': timezone.now()
        }
    )
    logger.info(f"{'Created' if created else 'Updated'} UserInvite for user {user.email}: date_of_exam={date_of_exam}, start_time_slot={start_time_slot}")

    # Email content
    candidate_name = user.full_name
    registration_id = user.registration_id
    password = user.dob.strftime('%d-%m-%Y') if user.dob else 'N/A'

    subject = f"Exam Details - Freshers Drive {current_year}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    text_content = f"""
    Dear {candidate_name},

    Greetings!

    In reference to your application for Freshers Drive {current_year}, we request you to kindly attend for the Preliminary Technical Test on {date_of_exam} at {slot_timings} at the below venue.

    Venue:
    Intelligenz IT Info Solutions Pvt Ltd
    Plot No 23 & 24, 1st Floor,
    Silicon Park, Silicon Valley,
    Beside ICICI Bank Lane,
    Madhapur, Hyderabad – 500 081
    Google Map: https://maps.app.goo.gl/xA2ZAbZyhYRjiEoA8

    Registration Details:
    Name: {candidate_name}
    Registration ID: {registration_id}
    Password: {password}
    Slot Timings: {slot_timings}

    Test Instructions:
    • The online test is of {total_duration} minutes duration:
      o {gt_duration} minutes – General Test ({gt_total_questions} Questions: Aptitude / Reasoning / Verbal Communication)
      o {tt_duration} minutes – Technical Test ({tt_total_questions} Questions: Coding & MCQs)
    • Candidates can choose one of the following technologies for the Technical Test:
      Java, Python, .Net, Frontend, QA, PHP, UI/UX
    • Please bring the following:
      o A copy of your Resume
      o A valid ID proof
      o A printout of this email
    • Kindly report to the venue 30 minutes before your scheduled time.
    For any further assistance, please feel free to contact us {contact_number} or email us @ resumes@intelligenzit.com.

    Thanks & Regards,
    HR Team
    """

    html_content = f"""
    <p>Dear {candidate_name},</p>

    <p>Greetings!</p>

    <p>In reference to your application for Freshers Drive {current_year}, we request you to kindly attend for the Preliminary Technical Test on <strong>{date_of_exam}</strong> at <strong>{slot_timings}</strong> at the below venue.</p>

    <p><strong>Venue:</strong><br>
    Intelligenz IT Info Solutions Pvt Ltd<br>
    Plot No 23 & 24, 1st Floor,<br>
    Silicon Park, Silicon Valley,<br>
    Beside ICICI Bank Lane,<br>
    Madhapur, Hyderabad – 500 081<br>
    <a href="https://maps.app.goo.gl/xA2ZAbZyhYRjiEoA8">Google Map</a></p>

    <p><strong>Registration Details:</strong><br>
    Name: {candidate_name}<br>
    Registration ID: {registration_id}<br>
    Password: {password}<br>
    Slot Timings: {slot_timings}</p>

    <p><strong>Test Instructions:</strong><br>
    • The online test is of <strong>{total_duration}</strong> minutes duration:<br>
        o <strong>{gt_duration}</strong> minutes – General Test ({gt_total_questions} Questions: Aptitude / Reasoning / Verbal Communication)<br>
        o <strong>{tt_duration}</strong> minutes – Technical Test ({tt_total_questions} Questions: Coding & MCQs)<br>
    • Candidates can choose one of the following technologies for the Technical Test:<br>
        o Java, Python, .Net, Frontend, QA, PHP, UI/UX<br>
    • Please bring the following:<br>
        o A copy of your Resume<br>
        o A valid ID proof<br>
        o A printout of this email<br>
    • Kindly report to the venue 30 minutes before your scheduled time.<br>
    For any further assistance, please feel free to contact us <strong>{contact_number}</strong> or email us @ <a href="mailto:resumes@intelligenzit.com">resumes@intelligenzit.com</a>.</p>

    <p>Thanks & Regards,<br>HR Team</p>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        user.is_mail_sent = True
        user.action_status = 'exam_details_sent'
        user.save(update_fields=['is_mail_sent', 'action_status'])
        logger.info(f"Exam details email sent successfully to {user.email}")
        messages.success(request, f"Exam details sent successfully to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send exam details email to {user.email}: {str(e)}")
        user.is_mail_sent = False
        user.action_status = 'pending'
        user.save(update_fields=['is_mail_sent', 'action_status'])
        messages.error(request, f"Failed to send exam details to {user.email}")

    return redirect(reverse('user_list') + '?page=' + request.GET.get('page', '1'))


@csrf_protect
def user_login(request):
    # Redirect if user already logged in
    if request.session.get('user_id'):
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']

            force_login = request.POST.get("force_login", "false") == "true"

            # ✅ Check if user already has active session
            if user.active_session_key and not force_login:
                try:
                    # If the old session still exists, block new login
                    old_session = Session.objects.get(session_key=user.active_session_key)
                    if old_session.expire_date > timezone.now():
                        # Instead of blocking, ask user to confirm force login
                        messages.warning(request, "already_logged_in")
                        return render(request, 'users/login.html', {
                            'form': form,
                            'show_force_popup': True,
                            'conflict_user_id': user.user_id,  # flag for template JS
                        })
                except Session.DoesNotExist:
                    pass  # old session invalid → allow normal login

            # ✅ If "force_login" chosen → kill old session
            if user.active_session_key and force_login:
                try:
                    Session.objects.filter(session_key=user.active_session_key).delete()
                    logger.info(f"Killed old session for {user.email}")
                except Exception as e:
                    logger.warning(f"Could not kill old session for {user.email}: {e}")

            # === Existing exam validations (unchanged) ===
            try:
                user_invite = UserInvite.objects.get(user=user, is_deleted=False)
            except UserInvite.DoesNotExist:
                messages.error(request, 'No valid invitation found. Please contact support.')
                logger.warning(f"Login attempt by {user.email} failed: No valid invitation found.")
                return render(request, 'users/login.html', {'form': form})

            # Get current date and time
            current_datetime = timezone.now()
            current_date = current_datetime.date()
            current_time = current_datetime.time()

            # Validate exam date
            if not user_invite.date_of_exam:
                messages.error(request, 'Exam date not set for your invitation. Please contact support.')
                logger.warning(f"Login attempt by {user.email} failed: Exam date not set.")
                return render(request, 'users/login.html', {'form': form})

            # Format date as DD-MM-YYYY for error message
            exam_date_formatted = user_invite.date_of_exam.strftime('%d-%m-%Y')
            if current_date != user_invite.date_of_exam:
                messages.error(request, f'Login is only allowed on your exam date: {exam_date_formatted}.')
                logger.warning(f"Login attempt by {user.email} failed: Current date {current_date} does not match exam date {user_invite.date_of_exam}.")
                return render(request, 'users/login.html', {'form': form})

            # Validate time slot
            if not user_invite.start_time_slot or not user_invite.end_time_slot:
                messages.error(request, 'Exam time slot not set for your invitation. Please contact support.')
                logger.warning(f"Login attempt by {user.email} failed: Time slot not set.")
                return render(request, 'users/login.html', {'form': form})

            # Convert time slots to 12-hour format for error message
            start_time_12hr = user_invite.start_time_slot.strftime('%I:%M %p').lstrip('0')
            end_time_12hr = user_invite.end_time_slot.strftime('%I:%M %p').lstrip('0')

            # Check if current time is outside the allowed time slot
            # Current time: 10:59 PM IST on 03-09-2025
            if not (user_invite.start_time_slot <= current_time <= user_invite.end_time_slot):
                messages.error(request, f'Login is only allowed between {start_time_12hr} and {end_time_12hr} on {exam_date_formatted}.')
                logger.warning(f"Login attempt by {user.email} failed: Current time {current_time} outside slot {user_invite.start_time_slot}-{user_invite.end_time_slot}.")
                return render(request, 'users/login.html', {'form': form})

            # ✅ If validation passes, proceed with login
            request.session['user_id'] = user.user_id
            request.session['registration_id'] = user.registration_id
            request.session['user_name'] = user.first_name
            request.session.set_expiry(7200)  # 2 hours session expiry

            # ✅ Ensure session has a key (important for server)
            if not request.session.session_key:
                request.session.create()

            session_key = request.session.session_key
            if not session_key:
                # fallback in rare cases when backend doesn’t assign one
                session_key = get_random_string(32)
                request.session['force_key'] = session_key
                request.session.save()
                logger.warning(f"Generated fallback session key for {user.email}: {session_key}")

            # ✅ Save session key to user
            user.active_session_key = session_key
            user.save(update_fields=['active_session_key'])
            
            messages.success(request, 'Logged in successfully.')
            logger.info(f"User {user.email} logged in successfully.")
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
            logger.warning(f"Login attempt failed: Invalid credentials for {request.POST.get('registration_id')}")
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})

@csrf_protect
def user_logout(request):
    if request.session.get('user_id'):
        try:
            user = Users.objects.get(user_id=request.session['user_id'])
            user.active_session_key = None
            user.save(update_fields=['active_session_key'])
        except Users.DoesNotExist:
            pass

    request.session.flush()
    messages.success(request, 'Logged out successfully.')
    return redirect('user_login')



def user_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    try:
        user = Users.objects.get(user_id=user_id, is_active=True, deleted=False)
    except Users.DoesNotExist:
        messages.error(request, 'User not found or account is inactive.')
        request.session.flush()
        return redirect('user_login')

    return render(request, 'users/dashboard.html', {
        'user': user,
        'user_name': request.session.get('user_name')
        })

@csrf_protect
def test_selection(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    try:
        user = Users.objects.get(user_id=user_id, is_active=True, deleted=False)
        # Check if general test is completed in database
        general_test_completed = Tests.objects.filter(
            user=user, 
            test_type='GT',
            is_submitted=True
        ).exists()
        
        context = {
            'user': user,
            'general_test_completed': general_test_completed,
            'technical_test_completed': Tests.objects.filter(
                user=user,
                test_type='TT',
                is_submitted=True
            ).exists()
        }
        return render(request, 'users/test_selection.html', context)
        
    except Users.DoesNotExist:
        return redirect('user_login')

@csrf_protect
def instructions_view(request, test_type):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, 'Please log in to view instructions.')
        return redirect('user_login')

    if not test_type or test_type not in ['GT', 'TT']:
        messages.error(request, 'Invalid or missing test type.')
        return redirect('test_selection')

    try:
        user = Users.objects.get(user_id=user_id, is_active=True, deleted=False)
        user_invite = UserInvite.objects.filter(user=user, is_mail_sent=True).order_by('-invitation_date').first()
        if not user_invite or not user_invite.date_of_exam or not user_invite.start_time_slot:
            messages.error(request, 'No valid exam schedule found. Please contact support.')
            return redirect('test_selection')

        login_window_minutes = get_config_value('login_window_duration', 10, int)
        try:
            start_datetime = datetime.combine(user_invite.date_of_exam, user_invite.start_time_slot)
        except TypeError as e:
            logger.error(f"Invalid date/time format for user {user.email}: date_of_exam={user_invite.date_of_exam}, start_time_slot={user_invite.start_time_slot}, error={str(e)}")
            messages.error(request, 'Invalid exam schedule data. Please contact support.')
            return redirect('test_selection')

        end_datetime = start_datetime + timedelta(minutes=login_window_minutes)
        start_time_display = start_datetime.strftime("%I:%M %p")
        end_time_display = end_datetime.strftime("%I:%M %p")
        exam_date_display = user_invite.date_of_exam.strftime("%Y-%m-%d")
        start_time_iso = start_datetime.isoformat()
        end_time_iso = end_datetime.isoformat()

        filtered_instructions = Instruction.objects.filter(
            test_type=test_type,
            is_active=True
        ).order_by('display_order', 'created_at')

        logger.debug(f"Test Type: {test_type}, Instructions Count: {filtered_instructions.count()}")

        test_type_display = dict(Instruction.TEST_TYPE_CHOICES).get(test_type, 'Test')

        return render(request, 'users/instructions.html', {
            'instructions': filtered_instructions,
            'test_type': test_type,
            'test_type_display': test_type_display,
            'user': user,
            'has_database_instructions': filtered_instructions.exists(),
            'start_time_display': start_time_display,
            'end_time_display': end_time_display,
            'exam_date_display': exam_date_display,
            'start_time_iso': start_time_iso,
            'end_time_iso': end_time_iso
        })
    except Users.DoesNotExist:
        messages.error(request, 'User not found or account is inactive.')
        request.session.flush()
        return redirect('user_login')
    except Exception as e:
        logger.error(f"Error in instructions_view for user {user_id}: {str(e)}")
        messages.error(request, 'An error occurred. Please contact support.')
        return redirect('test_selection')


@csrf_protect
def start_exam(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.warning(request, 'Please log in to start the exam.')
        return redirect('user_login')

    test_type = request.GET.get('test_type')
    if not test_type or test_type not in ['GT', 'TT']:
        messages.error(request, 'Invalid or missing test type.')
        return redirect('test_selection')

    try:
        user = Users.objects.get(user_id=user_id, is_active=True, deleted=False)
    except Users.DoesNotExist:
        messages.error(request, 'User not found or account is inactive.')
        request.session.flush()
        return redirect('user_login')



    # Store test_type in session for further processing
    request.session['test_type'] = test_type

    return render(request,  'start_test' , {
        'user': user,
        'test_type': test_type,
        # 'questions': questions,
        'test_type_display': dict(Instruction.TEST_TYPE_CHOICES).get(test_type, 'Test')
    })

from django.http import JsonResponse
@csrf_protect
def check_registration_id(request):
    if request.method == 'GET':
        reg_id = request.GET.get('registration_id')
        if reg_id:
            exists = Users.objects.filter(registration_id=reg_id).exists()
            return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})


@csrf_protect
def language_selection(request):
    # Session validation
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    # Check General Test completion
    
    return redirect('instructions_view', test_type='TT')
        
@csrf_protect
def submit_test(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('user_login')

        try:
            user = Users.objects.get(user_id=user_id)
            # Update or create test record with is_submitted=1
            test, created = Tests.objects.update_or_create(
                user=user,
                test_type='GT',  # General Test
                defaults={
                    'is_submitted': True,
                    'submission_time': timezone.now(),
                    'end_time': timezone.now(),
                    'test_name': 'General Test'
                }
            )
            messages.success(request, 'Test submitted successfully!')
            return redirect('test_selection')
            
        except Users.DoesNotExist:
            return redirect('user_login')

from .models import FinalResult

def user_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login')

    try:
        user = Users.objects.get(user_id=user_id, is_active=True, deleted=False)
    except Users.DoesNotExist:
        messages.error(request, 'User not found or account is inactive.')
        request.session.flush()
        return redirect('user_login')

    # Check status of General Test and Technical Test
    general_test_done = Tests.objects.filter(user=user, test_type='GT', is_submitted=True).exists()
    technical_test_done = Tests.objects.filter(user=user, test_type='TT', is_submitted=True).exists()

    if general_test_done and technical_test_done:
        exam_status = "Thank you! We will get back to you soon."
    else:
        exam_status = "Ready to Start"

    return render(request, 'users/dashboard.html', {
        'user': user,
        'exam_status': exam_status,
        'user_name': request.session.get('user_name')
    })
@csrf_exempt
def capture_photo(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'error': 'User not authenticated'})
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            try:
                user = Users.objects.get(user_id=user_id)
                reg_id = user.registration_id
                # Save in media/<registration_id>/exam_photo.<ext>
                user_folder = os.path.join(settings.MEDIA_ROOT, reg_id)
                os.makedirs(user_folder, exist_ok=True)
                file_name = f"exam_photo.{ext}"
                file_path = os.path.join(reg_id, file_name)
                data = ContentFile(base64.b64decode(imgstr), name=file_name)
                user.camera_photo.save(file_path, data)
                user.save()
                return JsonResponse({'success': True})
            except Users.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'User not found'})
        return JsonResponse({'success': False, 'error': 'No image data'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from home.users.models import Users
from django.contrib.gis.geoip2 import GeoIP2


@csrf_exempt
def update_location(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if not user_id:
            return JsonResponse({"success": False, "error": "User not logged in"})
        
        try:
            user = Users.objects.get(user_id=user_id)
        except Users.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"})
        
        # Get client IP
        ip_address = get_client_ip(request)
        user.ip_address = ip_address

        lat = request.POST.get("latitude")
        lng = request.POST.get("longitude")

        if lat and lng:
            # Case 1: User allowed location
            try:
                user.latitude = float(lat)
                user.longitude = float(lng)
                user.save()
                return JsonResponse({"success": True, "method": "browser"})
            except ValueError:
                return JsonResponse({"success": False, "error": "Invalid coordinates"})
        else:
            # Case 2: Fallback to IP-based location
            try:
                g = GeoIP2()
                location = g.city(ip_address)
                user.latitude = location.get("latitude")
                user.longitude = location.get("longitude")
                user.save()
                return JsonResponse({"success": True, "method": "ip"})
            except Exception as e:
                return JsonResponse({"success": False, "error": f"IP lookup failed: {str(e)}"})
    
    return JsonResponse({"success": False, "error": "Invalid request"})


def get_client_ip(request):
    """Get client IP considering proxies/load balancers"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

