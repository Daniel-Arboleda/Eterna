# password_reset/views.py

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now, timedelta
from .models import PasswordResetToken

User = get_user_model()

MAX_ATTEMPTS = 3 # Máximo de intentos por hora

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "El email es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si el usuario ha hecho demasiadas solicitudes en la última hora
        one_hour_ago = now() - timedelta(hours=1)
        recent_requests = PasswordResetToken.objects.filter(user=user, created_at__gte=one_hour_ago)

        if recent_requests.count() >= MAX_ATTEMPTS:
            return Response({"error": "Demasiados intentos. Intenta más tarde."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Eliminar tokens antiguos no usados
        PasswordResetToken.objects.filter(user=user, used=False).delete()

        # Crear un nuevo token
        token = PasswordResetToken.objects.create(
            user=user,
            expires_at=now() + timedelta(minutes=30),
            ip_address=request.META.get('REMOTE_ADDR')
        )

        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token.token}"

        # Enviar correo con el enlace de restablecimiento
        send_mail(
            "Restablecimiento de contraseña",
            f"Hola, usa el siguiente enlace para restablecer tu contraseña: {reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "Se ha enviado un correo con las instrucciones."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    def post(self, request, token):
        new_password = request.data.get("password")
        if not new_password:
            return Response({"error": "La nueva contraseña es obligatoria."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset_token = PasswordResetToken.objects.get(token=token, used=False)
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Token inválido o ya utilizado."}, status=status.HTTP_400_BAD_REQUEST)

        if reset_token.is_expired():
            return Response({"error": "Token expirado."}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_token.user
        user.set_password(new_password)
        user.save()

        # Marcar el token como usado
        reset_token.mark_as_used()

        return Response({"message": "Contraseña restablecida con éxito."}, status=status.HTTP_200_OK)
