from rest_framework import viewsets, permissions
from .models import Consulta
from .serializers import ConsultaSerializer
from usuarios.permissions import IsProfissionalSaude
from usuarios.models import UserRole

class ConsultaViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultaSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfissionalSaude]

    def get_queryset(self):
        user = self.request.user
        base_queryset = Consulta.objects.select_related(
            'agendamento__paciente', 'profissional_responsavel', 'criado_por', 'modificado_por'
        )
        # Ensure user is authenticated and is a health professional
        if user.is_authenticated and hasattr(user, 'role') and user.role == UserRole.PROFISSIONAL_SAUDE:
            # Filter consultations to only those where the current user is the responsible professional
            return base_queryset.filter(profissional_responsavel=user)
        # If not a health professional or not authenticated, return no consultations
        # Or, depending on requirements, could raise PermissionDenied or allow admin to see all.
        # For this requirement, strictly only the responsible professional sees their consultations.
        return Consulta.objects.none()

    # Pass request to serializer context to access user for audit and logic
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
