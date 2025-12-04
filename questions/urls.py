from django.urls import path
from . import views

urlpatterns = [
        path('', views.question_list, name='question_list'),
        path('add/', views.question_add, name='question_add'),
        path('edit/<int:question_id>/', views.question_edit, name='question_edit'),
        path('delete/<int:question_id>/', views.question_delete, name='question_delete'),
        path('questions/import/', views.question_import, name='question_import'),
        path('download-reference/', views.download_reference_excel, name='download_reference_excel'),
    ]