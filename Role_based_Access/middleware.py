from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import resolve
import re
from .models import Employee

class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Define public URLs accessible to everyone (including unauthenticated users)
        public_urls = [
            '/',
            '/admin/login/',
            '/admin/logout/',
            '/admin/'
        ]

        # Get the current URL path (relative path)
        current_url = request.path.rstrip('/')

        # Allow access to public URLs for all users
        if current_url in [url.rstrip('/') for url in public_urls]:
            return None

        # Allow superusers full access
        if request.user.is_superuser:
            return None

        # For authenticated users, check department-based permissions
        if request.user.is_authenticated:
            try:
                employee = Employee.objects.get(user=request.user)
                department = employee.department.lower()

                # Hardcoded allowed URLs per department
                allowed_urls = {
                    'hr': [
                        '/users/list/',
                        '/results/',
                        '/final-results/',
                        '/generate-test/'
                    ],
                    'programming team': [
                        '/tests/',
                        '/tests/view/'  # Base path for /tests/view/<int:pk>/
                    ]
                }

                # Collect allowed URLs for the user's department
                user_allowed_urls = allowed_urls.get(department, [])

                # Check if the current URL is allowed
                is_allowed = False
                for allowed_url in user_allowed_urls:
                    allowed_url = allowed_url.rstrip('/')
                    if allowed_url == current_url:
                        is_allowed = True
                        break
                    # Check for dynamic URL pattern /tests/view/<int:pk>/
                    if allowed_url == '/tests/view' and re.match(r'^/tests/view/\d+/?$', current_url):
                        is_allowed = True
                        break

                if user_allowed_urls and not is_allowed:
                    return render(request, 'Role_based_Access/error.html', status=403)

            except Employee.DoesNotExist:
                # If no Employee record exists, deny access
                return render(request, 'Role_based_Access/error.html', status=403)

        # Allow unauthenticated users to proceed (e.g., for login page redirection by Django)
        return None