from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pacientes.views import PacienteViewSet
from agendamentos.views import AgendamentoViewSet
from consultas.views import ConsultaViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'agendamentos', AgendamentoViewSet, basename='agendamento')
router.register(r'consultas', ConsultaViewSet, basename='consulta')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Documentação Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Views que não usam ViewSet (usuários)
    path('api/usuarios/', include('usuarios.urls')),

    # Todas as rotas de pacientes, agendamentos e consultas via ViewSet
    path('api/', include(router.urls)),
]
