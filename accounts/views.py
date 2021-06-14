from rest_framework.views import APIView
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