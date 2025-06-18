from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer
from .permissions import IsAdminUser # Import the custom permission

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # TODO: SECURITY RISK - Currently, any authenticated user can list all other users.
    # This endpoint should typically be restricted to admin users.
    # Consider changing to: permission_classes = [IsAdminUser] (or your specific admin permission)
    # If this endpoint is intended for the logged-in user to fetch their own data,
    # that should be a separate endpoint like /api/usuarios/me/ that returns request.user.
    # The AuthContext.jsx frontend currently misuses this endpoint for fetching user data.
    permission_classes = [permissions.IsAuthenticated] # Use the custom admin role permission

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # TODO: SECURITY RISK - Currently, any authenticated user can view details of any other user by ID.
    # This should typically be restricted to admins or the user themselves.
    # Consider changing to a permission like:
    # permission_classes = [IsOwnerOrAdminOrReadOnly] (custom permission needed)
    # or ensure this is only accessible by admins if that's the intent.
    permission_classes = [permissions.IsAuthenticated] # Also protect detail view by Admin

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny] # Anyone can register
