from django.contrib import admin
from django.urls import path, include
from .views import SignUpView, ProfileView, LoginView, LogOutView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('signup/', SignUpView.as_view())
]