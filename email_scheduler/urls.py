from django.urls import path
from . import views

urlpatterns = [
    path("export-tests-excel", views.export_tests_excel, name="export_tests_excel"),
    path("export-exam-summary", views.export_exam_summary, name="export_exam_summary"),
    path("export-browser-details", views.export_browser_details, name="export_browser_details"),
]
