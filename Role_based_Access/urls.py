from django.urls import path
from . import views

urlpatterns = [
        path('', views.manage_employees, name='manage_employees'),
        path('manage_roles/', views.manage_employees, name='manage_employees'),
        path('employees/add/', views.add_employee, name='add_employee'),
        path('employees/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
        path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
        
     ]