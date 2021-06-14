from rest_framework import serializers
from django.db import models
from .models import Voting, Choice, Vote
from accounts.serializers import UserSerializer

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

        def create(self, validated_data):
            return Choice.objects.create(**validated_data)

        def update(self, validated_data):
            return Choice.objects.create(**validated_data)

class VotingSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    class Meta:
        model = Voting
        fields = '__all__'

        def create(self, validated_data, context):
            return Voting.objects.create(**validated_data)

        def update(self, validated_data):
            return Voting.objects.create(**validated_data)

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

        def create(self, validated_data):
            return Vote.objects.create(**validated_data)

        def update(self, validated_data):
            return Vote.objects.create(**validated_data)
