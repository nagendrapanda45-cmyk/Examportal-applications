from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps
from Role_based_Access.models import Employee

def module_access_required(*module_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            try:
                employee = Employee.objects.get(user=request.user)
                if any(mod in employee.accessible_modules for mod in module_names):
                    return view_func(request, *args, **kwargs)
            except Employee.DoesNotExist:
                pass
            raise PermissionDenied
        return _wrapped_view
    return decorator
