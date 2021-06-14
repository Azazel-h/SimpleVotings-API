from django.contrib import admin
from django.urls import path, include
from .views import SignUpView

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('signup', SignUpView.as_view())
]