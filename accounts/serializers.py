from rest_framework import serializers
from django.contrib.auth.models import User

from django.db import models

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        self.validate(validated_data)
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        return user