# users/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import User

def register(request):
    # Lógica para registrar un usuario
    return JsonResponse({"message": "User registered successfully"})

def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({'username': user.username, 'email': user.email})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def login(request):
    # Aquí iría tu lógica de login, por ejemplo, autenticación de usuarios.
    return JsonResponse({'message': 'Login endpoint'})

def profile(request):
    # Lógica para obtener el perfil del usuario
    # Aquí podrías usar algo como:
    user = request.user  # Suponiendo que ya estás autenticado
    return JsonResponse({
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    })
