from django.urls import path
from . import views

app_name = 'qr_generator'

urlpatterns = [
    path('list/', views.qr_list, name='qr_list'),
    path('create/', views.qr_create, name='qr_create'),  # <-- new
    path('<int:pk>/details/', views.qr_detail, name='qr_detail'),
    path('<int:pk>/regenerate/', views.regenerate_qr, name='qr_regenerate'),
    path('<int:pk>/delete/', views.qr_delete, name='qr_delete'),
]
