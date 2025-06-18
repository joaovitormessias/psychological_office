from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer
from .permissions import IsAdminUser # Import the custom permission

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # Use the custom admin role permission

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # Also protect detail view by Admin

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny] # Anyone can register
