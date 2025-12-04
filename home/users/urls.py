from django.urls import path
from . import views
from home.users.views import update_location

urlpatterns = [
    path('pdf/<int:pk>/', views.user_pdf_view, name='user_pdf'),
    path('list/', views.user_list_view, name='user_list'),
    path('create/', views.user_create_view, name='user_create'),
    path('edit/<int:pk>/', views.user_edit_view, name='user_edit'),
    path('delete/<int:pk>/', views.user_delete_view, name='user_delete'),
    path('users/<int:pk>/send-exam-details/', views.send_exam_details, name='send_exam_details'),
    # Geetha urls
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    
    # User Dashboard and Exam
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('test_selection/', views.test_selection, name='test_selection'),
    path('language_selection/',views.language_selection,name='language_selection'),
    path('instructions/<str:test_type>/', views.instructions_view, name='instructions_view'),
    path('start-exam/', views.start_exam, name='start_exam'),
    path('submit-test/',views.submit_test,name='submit_test'),
    path('check-registration/', views.check_registration_id, name='check_registration_id'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('capture-photo/', views.capture_photo, name='capture_photo'),
    path('update_location/', update_location, name='update_location'),

]
