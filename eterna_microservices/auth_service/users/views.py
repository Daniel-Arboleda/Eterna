from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes

# Vista para registrar un usuario
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    def post(self, request):
        User = get_user_model()
        data = request.data

        email = data.get('email')
        password = data.get('password')

        # Verificar si los campos están vacíos
        if not email or not password:
            return Response(
                {'error': 'El campo email y contraseña son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar si el correo electrónico ya está registrado
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'El correo electrónico ya está registrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener el username (si no se proporciona, usar el email como username)
        username = data.get('username', email)  # Si no se pasa 'username', se usa el email

        try:
            # Crear el usuario
            user = User.objects.create_user(email=email, password=password, username=username)  # Añadir el 'username'

            # Generar tokens JWT para el nuevo usuario
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Usuario creado con éxito.',
                'user_id': user.id,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Manejo de errores
            return Response(
                {'error': f'Ocurrió un error al crear el usuario: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




# Vista para obtener datos de la cuenta del usuario autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account(request):
    """
    Retorna los datos básicos de la cuenta del usuario autenticado:
    - email
    - date_joined
    """
    user = request.user  # Usuario autenticado
    return Response({
        'id': user.id,
        'email': user.email,
        'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        # 'created_at': user.create_at
    }, status=status.HTTP_200_OK)

# Vista para obtener un usuario por ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    """
    Obtener información básica de un usuario por ID.
    """
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)

        return Response({
            'id': user.id,
            'email': user.email,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            # 'role': rele.name
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
