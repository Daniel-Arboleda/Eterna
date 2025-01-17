from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework import status

class InvalidateTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Lógica para invalidar el token
        return Response({'detail': 'Token invalidado correctamente'})


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except InvalidToken as e:
            return Response(
                {'error': 'Token inválido o expirado', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )



class ObtainTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')  # Cambiado de 'username' a 'email'
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)  # Especificar 'email'
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)



class RevokeAllTokensView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Lógica para revocar todos los tokens del usuario
        return Response({'detail': 'Todos los tokens han sido revocados correctamente'})
