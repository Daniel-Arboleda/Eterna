# sessions/views.py

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
@permission_classes([AllowAny])  # Permitir acceso público
def login(request):
    # Leer datos del cuerpo de la solicitud
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Autenticar al usuario con el correo electrónico
    try:
        user = User.objects.get(email=email)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Vista para manejar el logout
@api_view(['POST'])
@permission_classes([AllowAny])  # O puedes restringir a usuarios autenticados con IsAuthenticated
def logout(request):
    auth_logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
