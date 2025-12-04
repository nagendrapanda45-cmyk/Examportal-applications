from django import template
from ..models import Employee

register = template.Library()

@register.filter
def is_programming_team(user):
    if not user.is_authenticated or user.is_superuser:
        return True
    try:
        employee = Employee.objects.get(user=user)
        return employee.department.lower() == 'programming team'
    except Employee.DoesNotExist:
        return False
 

@register.filter
def is_hr_team(user):
    if not user.is_authenticated or user.is_superuser:
        return True
    try:
        employee = Employee.objects.get(user=user)
        return employee.department.lower() == 'hr'
    except Employee.DoesNotExist:
        return False