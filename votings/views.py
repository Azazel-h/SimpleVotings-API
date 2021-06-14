from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Voting, Choice, Vote
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import VotingSerializer, ChoiceSerializer, VoteSerializer

class VotingsListView(APIView):
    def get(self, request):
        votings = Voting.objects.all()
        serializer = VotingSerializer(votings, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data["author"] = request.user.id
        serializer = VotingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class VotingDetailView(APIView):
    def get(self, request, pk):
        voting = Voting.objects.get(pk=pk)
        serializer = VotingSerializer(voting)
        return Response(serializer.data)

    def post(self, request, pk):
        data = request.data
        data['voting'] = pk
        serializer = ChoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
