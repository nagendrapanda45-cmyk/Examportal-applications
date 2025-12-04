from django.urls import path
from . import views


urlpatterns = [
    path('invite/', views.user_invite_list_view, name='user_invite_list'),
    path('invite/send-bulk-email/', views.send_bulk_email, name='send_bulk_email'),
    path('email-templates/', views.email_template_list, name='email_template_list'),
    path('email-templates/create/', views.email_template_create, name='email_template_create'),
    path('email-templates/edit/<int:email_id>/', views.email_template_edit, name='email_template_edit'),
    path('email-templates/delete/<int:email_id>/', views.email_template_delete, name='email_template_delete'),
    path('user/confirmation/<str:registration_id>/<str:confirmation_token>/', views.confirm_registration, name='confirm_registration'),
    path('download-bulk-pdfs/', views.download_bulk_pdfs, name='download_bulk_pdfs'),
]