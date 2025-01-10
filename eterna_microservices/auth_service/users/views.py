# users/views.py


from django.shortcuts import render
from django.http import JsonResponse
from .models import User

def register(request):
    # Lógica para registrar un usuario
    return JsonResponse({"message": "User registered successfully"})
