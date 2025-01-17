from django.urls import path, include
from .views import HealthCheckView, MicroserviceInfoView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('info/', MicroserviceInfoView.as_view(), name='microservice_info'),
    # Nota: Aquí no se incluyen rutas como users, porque ya están en urls.py general
    path('token/', include('auth_service.api.token.urls')),

]
