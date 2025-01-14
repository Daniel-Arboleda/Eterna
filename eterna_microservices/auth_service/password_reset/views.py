# password_reset/views.py

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

def request_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode()).decode()
            
            reset_link = request.build_absolute_uri(
                f'/password_reset/confirm/?uid={uid}&token={token}'
            )
            
            send_mail(
                'Password Reset Request',
                f'Please click the following link to reset your password: {reset_link}',
                'from@example.com',  # Replace with a valid email
                [user.email],
            )
            return JsonResponse({'message': 'Password reset link sent to email'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Email not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def confirm_reset(request):
    uid = request.GET.get('uid')
    token = request.GET.get('token')

    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            # Aquí puedes implementar la lógica de cambio de contraseña
            return JsonResponse({'message': 'Password reset link is valid'})
        else:
            return JsonResponse({'error': 'Invalid token or expired'}, status=400)
    except (User.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Invalid request'}, status=400)
