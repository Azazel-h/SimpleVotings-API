from django.contrib.auth.models import User
from django.http import QueryDict
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Voting, Choice, Vote
from rest_framework.response import Response
from .serializers import VotingSerializer, ChoiceSerializer, VoteSerializer


class VotingsListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        votings = Voting.objects.all()
        serializer = VotingSerializer(votings, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = QueryDict.copy(request.data)
        data["author"] = request.user.id
        serializer = VotingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class VotingDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        voting = get_object_or_404(Voting ,pk=pk)
        serializer = VotingSerializer(voting)
        return Response(serializer.data)

    def put(self, request, pk):
        data = QueryDict.copy(request.data)
        data['voting'] = pk
        serializer = ChoiceSerializer(data=data)
        valid = serializer.is_valid()
        if get_object_or_404(Voting, pk=pk).author == request.user:
            if valid:
                serializer.save()
                return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, pk):
        data = QueryDict.copy(request.data)
        voting = Voting.objects.get(pk=pk)
        choice = get_object_or_404(Choice.objects.filter(voting=pk), pk=request.data['choice'])
        data['user'] = request.user.id
        serializer = VoteSerializer(data=data)
        valid = serializer.is_valid()

        if voting.type == 0:
            if not Vote.objects.filter(choice__in=Choice.objects.filter(voting=pk), user=data['user']):
                if self.valid(valid, voting, serializer):
                    return Response(serializer.data, status=201)
        elif voting.type == 1:
            if not Vote.objects.filter(choice=choice, user=data['user']):
                if self.valid(valid, voting, serializer):
                    return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def valid(self, valid, voting, serializer):
        if valid:
            voting.total_votes += 1
            voting.save()
            serializer.save()
            return True
        return False

