from django.db import models
from django.contrib.auth.models import User

class Voting(models.Model):
    title = models.CharField(max_length=65)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Choice(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=65)

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)