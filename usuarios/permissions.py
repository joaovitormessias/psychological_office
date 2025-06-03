from rest_framework.permissions import BasePermission
from .models import UserRole

class IsSecretaria(BasePermission):
    """
    Allows access only to users with the SECRETARIA role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.SECRETARIA)

class IsProfissionalSaude(BasePermission):
    """
    Allows access only to users with the PROFISSIONAL_SAUDE role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.PROFISSIONAL_SAUDE)

class IsAdminUser(BasePermission): # Re-using Django's IsAdminUser name but for our role
    """
    Allows access only to users with the ADMIN role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.ADMIN)
