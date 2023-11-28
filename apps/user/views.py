from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import User
from .serializers import UserSerializer


# Create your views here.
class Register(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return current user details
        """
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
