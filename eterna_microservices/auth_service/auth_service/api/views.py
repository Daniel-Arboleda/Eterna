# auth_service/api/views.py


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class HealthCheckView(APIView):
    """
    Verifica que el microservicio está corriendo.
    """
    permission_classes = [permissions.AllowAny]  # Permitir acceso sin autenticación
    def get(self, request):
        return Response({"status": "OK", "message": "Auth Service is running"}, status=status.HTTP_200_OK)


class MicroserviceInfoView(APIView):
    """
    Proporciona información básica del microservicio.
    """
    permission_classes = [permissions.AllowAny]  # Permitir acceso sin autenticación
    def get(self, request):
        return Response({
            "service_name": "Auth Service",
            "description": "Microservicio para autenticación y gestión de usuarios",
            "version": "1.0.0",
        }, status=status.HTTP_200_OK)
