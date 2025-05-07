
from django.contrib import admin
from django.urls import path,include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.routers import DefaultRouter
from psychological_office import views


router  = DefaultRouter()
router.register(r'patients', views.PatientViewSet)
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'consultations', views.ConsultationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include(router.urls)),
]   
