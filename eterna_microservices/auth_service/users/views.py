from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from roles.models import Role
from .token_storage import TokenManager


# Vista para registrar un usuario con múltiples roles
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        User = get_user_model()
        data = request.data

        email = data.get('email')
        password = data.get('password')
        role_names = data.get('roles', ['Cliente'])  # Lista de roles, por defecto "Cliente"

        if not email or not password:
            return Response({'error': 'El campo email y contraseña son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'El correo electrónico ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)

        username = data.get('username', email)

        try:
            roles = Role.objects.filter(name__in=role_names)  # Buscar todos los roles por nombre
            if not roles.exists():
                return Response({'error': 'Uno o más roles no son válidos.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(email=email, password=password, username=username, roles=roles)

            return Response({
                'message': 'Usuario creado con éxito.',
                'user_id': user.id,
                'roles': [role.name for role in user.roles.all()],
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Ocurrió un error al crear el usuario: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Vista para obtener los roles de un usuario autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_roles(request):
    user = request.user
    return Response({'roles': [role.name for role in user.roles.all()]}, status=status.HTTP_200_OK)


# Vista para obtener datos de la cuenta del usuario autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account(request):
    """
    Retorna los datos básicos de la cuenta del usuario autenticado:
    - id
    - email
    - date_joined
    """
    user = request.user
    return Response({
        'id': user.id,
        'email': user.email,
        'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
    }, status=status.HTTP_200_OK)


# Vista para obtener un usuario por ID, permitiendo que los administradores accedan a cualquier usuario
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    """
    Obtener información básica de un usuario por su ID.
    Los administradores pueden acceder a cualquier usuario.
    Un usuario regular solo puede acceder a su propia información.
    """
    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)

        # Verificar si el usuario autenticado es administrador o si está accediendo a su propia información
        if request.user.id != user.id and not request.user.roles.filter(name="Administrador").exists():
            return Response({'error': 'No tienes permiso para acceder a esta información.'}, status=status.HTTP_403_FORBIDDEN)

        return Response({
            'id': user.id,
            'email': user.email,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
