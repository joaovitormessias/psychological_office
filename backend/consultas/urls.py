from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultaViewSet

router = DefaultRouter()
router.register(r'', ConsultaViewSet, basename='consulta')

urlpatterns = [
    path('', include(router.urls)),
]
