from django.urls import path
from . import views
from home.users.views import update_location

urlpatterns = [
    path('pdf/<int:pk>/', views.user_pdf_view, name='user_pdf'),
    path('pdf/<int:pk>/', views.user_pdf_view, name='candidate_pdf'),
    path('list/', views.candidate_list_view, name='user_list'),
    path('list/', views.candidate_list_view, name='candidate_list'),
    path('create/', views.user_create_view, name='user_create'),
    path('create/', views.user_create_view, name='candidate_create'),
    path('edit/<int:pk>/', views.user_edit_view, name='user_edit'),
    path('edit/<int:pk>/', views.user_edit_view, name='candidate_edit'),
    path('delete/<int:pk>/', views.user_delete_view, name='user_delete'),
    path('delete/<int:pk>/', views.user_delete_view, name='candidate_delete'),
    path('users/<int:pk>/send-exam-details/', views.send_exam_details, name='send_exam_details'),
    # Geetha urls
    path('register/', views.candidate_register, name='candidate_register'),
    path('register/', views.candidate_register, name='user_register'),
    path('login/', views.candidate_login, name='candidate_login'),
    path('login/', views.candidate_login, name='user_login'),
    path('logout/', views.candidate_logout, name='candidate_logout'),
    path('logout/', views.candidate_logout, name='user_logout'),
    
    # User Dashboard and Exam
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/', views.user_dashboard, name='candidate_dashboard'),
    path('test_selection/', views.test_selection, name='test_selection'),
    path('language_selection/',views.language_selection,name='language_selection'),
    path('instructions/<str:test_type>/', views.instructions_view, name='instructions_view'),
    path('instructions/', views.instructions_view, {'test_type': 'GT'}, name='instructions'),
    path('instructions/', views.instructions_view, {'test_type': 'GT'}, name='exam_instructions'),
    path('start-exam/', views.start_exam, name='start_exam'),
    path('submit-test/',views.submit_test,name='submit_test'),
    path('check-registration/', views.check_registration_id, name='check_registration_id'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('submit-registration-feedback/', views.submit_registration_feedback, name='submit_registration_feedback'),
    path('capture-photo/', views.capture_photo, name='capture_photo'),
    path('update_location/', update_location, name='update_location'),
]
