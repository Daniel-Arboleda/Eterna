# two_factor_auth/views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import TwoFactorAuth
import pyotp

def enable_2fa(request):
    if request.method == 'POST':
        user = request.user
        two_factor_auth, created = TwoFactorAuth.objects.get_or_create(user=user)
        if not two_factor_auth.is_enabled:
            two_factor_auth.generate_secret_key()
            two_factor_auth.is_enabled = True
            two_factor_auth.save()
            return JsonResponse({'message': 'Two-factor authentication enabled successfully'})
        return JsonResponse({'error': '2FA is already enabled'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def verify_2fa(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user = request.user
        two_factor_auth = get_object_or_404(TwoFactorAuth, user=user)
        if two_factor_auth.verify_code(code):
            return JsonResponse({'message': 'Two-factor authentication verified successfully'})
        return JsonResponse({'error': 'Invalid code'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)
