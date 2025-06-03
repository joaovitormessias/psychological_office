from rest_framework import viewsets, permissions, filters
from .models import Agendamento
from .serializers import AgendamentoSerializer
from usuarios.permissions import IsSecretaria, IsProfissionalSaude
from django_filters.rest_framework import DjangoFilterBackend

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all().select_related('paciente', 'criado_por', 'modificado_por')
    serializer_class = AgendamentoSerializer
    permission_classes = [permissions.IsAuthenticated, (IsSecretaria | IsProfissionalSaude)]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = { # More specific filtering
        'paciente__id': ['exact'],
        'paciente__nome': ['icontains'],
        'data': ['exact', 'gte', 'lte', 'range'],
        'status': ['exact'],
    }
    search_fields = ['paciente__nome', 'observacoes'] # Search by patient name or observations
    ordering_fields = ['data', 'hora', 'paciente__nome', 'status']

    # To automatically set criado_por/modificado_por
    def perform_create(self, serializer):
        # criador_por is handled in serializer create method from context
        serializer.save() # User is passed via context to serializer

    def perform_update(self, serializer):
        # modificado_por is handled in serializer update method from context
        serializer.save() # User is passed via context to serializer

    # To provide request to the serializer context
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
