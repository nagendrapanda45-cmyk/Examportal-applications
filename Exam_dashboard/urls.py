from django.urls import path
from . import views

urlpatterns = [
    # General Test URLs
    path('start_test/', views.start_test, name='start_test'),
    path('test_page/', views.test_page, name='test_page'),
    path('submit_test/', views.submit_test, name='submit_test'),
    # Technical Test URLs
    path('select_language/', views.select_language, name='select_language'),
    path('start_technical_test/', views.start_technical_test, name='start_technical_test'),
    path('technical_test_page/', views.technical_test_page, name='technical_test_page'),
    path('submit_technical_test/', views.submit_technical_test, name='submit_technical_test'),
    # path('update_suspicious_activity/', views.update_suspicious_activity, name='update_suspicious_activity'),
    path('update_test_location/', views.update_test_location, name='update_test_location'),
    # path('update_resolution_mismatch/', views.update_resolution_mismatch, name='update_resolution_mismatch'),
    path('capture_screenshot/', views.captureScreenshot, name='captureScreenshot'),
    path('log_browser/', views.log_browser, name='log_browser'),
]