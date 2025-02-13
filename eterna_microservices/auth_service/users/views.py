import uuid
import logging
from django.core.mail import send_mail, EmailMessage
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from roles.models import Role
import re  # Para las expresiones regulares

# Configuración de logging
logger = logging.getLogger(__name__)

# Función para validar el formato del correo
def validate_user_email(email):
    try:
        validate_email(email)
    except ValidationError:
        raise Exception('El correo electrónico no es válido.')

# Función para enviar el correo de bienvenida
def send_welcome_email(user_email):
    try:
        # Generamos un UUID único para el Message-ID
        unique_id = uuid.uuid4().hex
        email = EmailMessage(
            'Bienvenido a Eterna',
            'Gracias por registrarte en Eterna. Estamos felices de tenerte con nosotros.',
            'no-reply@eterna.com',
            [user_email],
            headers={'Message-ID': f'<{unique_id}@eterna.com>'}
        )
        email.send()
        logger.info(f"Correo de bienvenida enviado a: {user_email}")
    except Exception as e:
        logger.error(f"Error al enviar correo a {user_email}: {e}")
        raise Exception(f"Error al enviar correo a {user_email}: {e}")  # Lanza el error para manejarlo en la vista

# Función para validar contraseñas robustas
def validate_password(password):
    # Requerimientos:
    # 1. Mínimo 8 caracteres
    # 2. Al menos una letra mayúscula
    # 3. Al menos una letra minúscula
    # 4. Al menos un número
    # 5. Al menos un carácter especial
    if len(password) < 8:
        raise Exception('La contraseña debe tener al menos 8 caracteres.')
    if not re.search(r'[A-Z]', password):
        raise Exception('La contraseña debe contener al menos una letra mayúscula.')
    if not re.search(r'[a-z]', password):
        raise Exception('La contraseña debe contener al menos una letra minúscula.')
    if not re.search(r'[0-9]', password):
        raise Exception('La contraseña debe contener al menos un número.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise Exception('La contraseña debe contener al menos un carácter especial.')
    
    return True

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        User = get_user_model()
        data = request.data

        # Obtención de datos de entrada
        email = data.get('email')
        password = data.get('password')
        role_names = data.get('roles', ['Cliente'])  # Lista de roles, por defecto "Cliente"

        # Validaciones iniciales
        if not email or not password:
            return Response({'error': 'El campo email y contraseña son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'El correo electrónico ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)

        username = data.get('username', email)

        try:
            # Validación del correo electrónico
            validate_user_email(email)
            
            # Validación de la contraseña
            validate_password(password)

            roles = Role.objects.filter(name__in=role_names)  # Buscar todos los roles por nombre
            if not roles.exists():
                return Response({'error': 'Uno o más roles no son válidos.'}, status=status.HTTP_400_BAD_REQUEST)

            # Crear el usuario
            user = User.objects.create_user(email=email, password=password, username=username)
            
            # Asignar roles correctamente
            user.roles.set(roles)

            # Enviar el correo de bienvenida
            send_welcome_email(user.email)

            return Response({
                'message': 'Usuario creado con éxito. Se ha enviado un correo de bienvenida.',
                'user_id': user.id,
                'roles': [role.name for role in user.roles.all()],
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error al crear el usuario: {str(e)}")
            return Response({'error': f'Ocurrió un error al procesar tu solicitud: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
