from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('notifications/', views.user_notifications, name='notifications'),
]
