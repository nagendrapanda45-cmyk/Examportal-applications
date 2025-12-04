"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from home.admin import custom_admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.core.exceptions import DisallowedHost
from django.http import HttpResponse
from django.shortcuts import render
# Custom error handlers
def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def handler403(request, exception):
    return render(request, '403.html', status=403)

def handler400(request, exception):
    return render(request, '400.html', status=400)


urlpatterns = [
    # path("admin/", admin.site.urls),
    # path('', include('home.urls_user')),  # Load user views
    path('', include('home.urls')),
    #path("", include('admin_material.urls')),
    path('users/', include('home.users.urls')),
    path('questions/', include('questions.urls')),
    path('exam_dashboard/', include('Exam_dashboard.urls')),
    path('qr/', include('qr_generator.urls')),
    path('admin/', custom_admin.urls),
    path('role_based_access/', include('Role_based_Access.urls')),
    path('invite/', include('user_invite.urls')),
    path('email_scheduler/', include('email_scheduler.urls')),
    # path('', include('django_prometheus.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
