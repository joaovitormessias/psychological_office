from rest_framework import viewsets, permissions, filters
from .models import Paciente
from .serializers import PacienteSerializer
from usuarios.permissions import IsSecretaria, IsProfissionalSaude
from django_filters.rest_framework import DjangoFilterBackend # For more advanced filtering if needed

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by('nome') # Ordem alfabética
    serializer_class = PacienteSerializer
    # Permissions: SECRETARIA or PROFISSIONAL_SAUDE
    permission_classes = [permissions.IsAuthenticated, (IsSecretaria | IsProfissionalSaude)]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'cpf', 'email'] # Fields for search
    ordering_fields = ['nome', 'criado_em'] # Fields available for ordering
    # filterset_fields = ['endereco_residencial__cidade', 'endereco_residencial__uf'] # Example for DjangoFilterBackend

    # To automatically set criado_por/modificado_por
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modificado_por=self.request.user)

    # Mock city filtering based on UF (could be a separate endpoint or action)
    # This is just a conceptual placeholder.
    # A real implementation might be a GET request to /api/v1/enderecos/cidades/?uf=SP
    # @action(detail=False, methods=['get'])
    # def cidades_por_uf(self, request):
    #     uf = request.query_params.get('uf')
    #     if not uf:
    #         return Response({"error": "UF parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    #     # Mock data
    #     cidades = {
    #         "SP": ["São Paulo", "Campinas", "Santos"],
    #         "RJ": ["Rio de Janeiro", "Niterói"],
    #         # ... other states
    #     }
    #     return Response(cidades.get(uf.upper(), []))
