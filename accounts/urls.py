from django.contrib import admin
from django.urls import path, include
from .views import SignUpView, ProfileView, LoginView, LogOutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('signup/', SignUpView.as_view(), name='signup')
]