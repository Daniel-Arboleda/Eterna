# auth_service/auth_service/api/token/urls.py


from django.urls import path
from .views import InvalidateTokenView, RefreshTokenView, ObtainTokenView, RevokeAllTokensView



urlpatterns = [
    path('invalidate/', InvalidateTokenView.as_view(), name='invalidate_token'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh_token'),
    path('obtain/', ObtainTokenView.as_view(), name='obtain_token'),
    path('revoke/', RevokeAllTokensView.as_view(), name='revoke_all_tokens'),
]
