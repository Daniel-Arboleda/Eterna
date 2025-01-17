from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

def generate_token(user):
    """
    Genera un JWT utilizando la librería simplejwt.
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def decode_token(token):
    """
    Decodifica un JWT.
    """
    from rest_framework_simplejwt.exceptions import TokenError
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def refresh_token(refresh_token):
    """
    Refresca el token usando el refresh token proporcionado.
    """
    try:
        refresh = RefreshToken(refresh_token)
        return str(refresh.access_token)
    except Exception:
        return None
