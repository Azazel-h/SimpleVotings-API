from django.contrib import admin
from django.urls import path, include
from .views import SignUpView, ProfileView

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('profile', ProfileView.as_view()),
    path('signup', SignUpView.as_view())
]