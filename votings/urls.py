from django.contrib import admin
from django.urls import path, include
from .views import VotingsListView, VotingDetailView

urlpatterns = [
    path('', VotingsListView.as_view()),
    path('<int:pk>', VotingDetailView.as_view())
]