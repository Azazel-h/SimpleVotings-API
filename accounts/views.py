from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from votings.models import Voting
from votings.serializers import VotingSerializer
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class SignUpView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get(self, request):
        votings = Voting.objects.filter(author=request.user)
        serializer = VotingSerializer(votings, many=True)
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=200)
        return Response({'error': 'Invalid Credentials'}, status=400)


class LogOutView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        user = request.user
        user.auth_token.delete()
        user.save()
        return Response(status=200)