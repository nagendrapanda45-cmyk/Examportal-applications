from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

class QuestionsAppAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path starts with the questions app URL
        if request.path.startswith('/questions/') and not request.user.is_authenticated:
            # Redirect to login page if user is not authenticated
            login_url = f"{settings.LOGIN_URL}?next={request.path}"
            return HttpResponseRedirect(login_url)
        
        return self.get_response(request)