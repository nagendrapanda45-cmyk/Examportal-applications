from django.urls import path,include
from . import views



from .views import (
    ConfigurationListView,
    ConfigurationCreateView,
    ConfigurationUpdateView,
    ConfigurationDeleteView
)
urlpatterns = [
    #Default path
    path('', views.index, name='index'),
    # Test URLs
    path('tests/', views.test_list, name='test_list'),
    path('tests/view/<int:pk>/', views.test_view, name='test_view'),
    path('tests/<int:pk>/edit/',views.test_edit,name='test_edit'),
    # Instruction URLs
    path('instructions/', views.instruction_list, name='instruction_list'),
    path('instructions/add/', views.instruction_add, name='instruction_add'),
    path('instructions/edit/<int:pk>/', views.instruction_edit, name='instruction_edit'),
    path('instructions/delete/<int:pk>/', views.instruction_delete, name='instruction_delete'),
    # results path
    path('results/', views.result_list, name='result_list'),
    path('result/<int:pk>/', views.result_view, name='result_view'),
    #generate test path
    path('generate-test/', views.generate_test, name='generate_test'),
    path('generate-answer-pdf/<int:pk>/', views.generate_answer_pdf, name='generate_answer_pdf'),
    path('download-test-sets-zip/', views.download_test_sets_zip, name='download_test_sets_zip'),
    path('final-results/', views.final_result_list, name='final_result_list'),
    path('final-results/<int:final_result_id>/view/', views.final_result_view, name='final_result_view'),
    path('final-results/<int:final_result_id>/edit/', views.final_result_edit, name='final_result_edit'),
    path('final-results/graphs/', views.final_result_graphs, name='final_result_graphs'),
    path('final-results/<int:final_result_id>/send-email/', views.send_result_email, name='send_result_email'),
 
    # configuration
    path('configurations/', ConfigurationListView.as_view(), name='configuration_list'),
    path('configurations/add/', ConfigurationCreateView.as_view(), name='configuration_add'),
    path('configurations/<int:pk>/edit/', ConfigurationUpdateView.as_view(), name='configuration_edit'),
    path('configurations/<int:pk>/delete/', ConfigurationDeleteView.as_view(), name='configuration_delete'),
    # import user 
    path('export/', views.export_users, name='export_users'),
    path('import/', views.import_status, name='import_status'),
    path('', views.index, name='index'),
]