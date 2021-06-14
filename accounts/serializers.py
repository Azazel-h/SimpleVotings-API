from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'