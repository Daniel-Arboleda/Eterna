# sessions/views.py

from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()  # Importar el modelo de usuario configurado


# Vista para manejar el login
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email y contraseña son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Inicio de sesión exitoso.',
                'access': access_token,
                'refresh': str(refresh),
                'roles': [role.name for role in user.roles.all()],  # Se incluyen los roles del usuario
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': f'Error al iniciar sesión: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    """
    Cierra la sesión del usuario.
    """
    auth_logout(request)
    return Response({'message': 'Sesión cerrada exitosamente.'}, status=status.HTTP_200_OK)