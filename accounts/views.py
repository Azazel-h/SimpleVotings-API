from rest_framework.views import APIView

from votings.models import Voting
from votings.serializers import VotingSerializer
from .serializers import UserSerializer
from rest_framework.response import Response

class SignUpView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.data, status=400)

class ProfileView(APIView):
    def get(self, request):
        votings = Voting.objects.filter(author=request.user)
        serializer = VotingSerializer(votings, many=True)
        return Response(serializer.data)