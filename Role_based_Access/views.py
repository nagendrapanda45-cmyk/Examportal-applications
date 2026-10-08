from Role_based_Access.decorators import module_access_required
# Role_based_Access/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import EmployeeForm, EmployeeEditForm
from .models import Employee
from django.db.models import Q

@login_required
@module_access_required('Manage Role')
def manage_employees(request):
    search_query = request.GET.get('search_query', '')
    employees = Employee.objects.all()
    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(department__icontains=search_query)  # Added department to search
        )

    return render(request, 'Role_based_Access/manage_employees.html', {
        'employees': employees,
        'search_query': search_query
    })

@login_required
@module_access_required('Manage Role')
def add_employee(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role added successfully!')
            return redirect('manage_employees')
        else:
            messages.error(request, 'Error adding role. Please check the form.')

    return render(request, 'Role_based_Access/add_employee.html', {
        'form': form
    })

@login_required
@module_access_required('Manage Role')
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        # Check if username was attempted to be changed
        if 'username' in request.POST and request.POST['username'] != employee.user.username:
            messages.error(request, 'Username cannot be changed.')
            return redirect('edit_employee', employee_id=employee.id)
            
        form = EmployeeEditForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role updated successfully!')
            return redirect('manage_employees')
        else:
            messages.error(request, 'Error updating role. Please check the form.')
    else:
        form = EmployeeEditForm(instance=employee)

    return render(request, 'Role_based_Access/edit_employee.html', {
        'form': form,
        'employee': employee
    })

@login_required
@module_access_required('Manage Role')
def delete_employee(request, employee_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=employee_id)
        user = employee.user
        employee.delete()
        user.delete()
        messages.success(request, 'Role deleted successfully!')
        return redirect('manage_employees')
    return redirect('manage_employees')