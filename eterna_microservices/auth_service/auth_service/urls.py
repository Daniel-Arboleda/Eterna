# auth_service/urls.py


from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('roles/', include('roles.urls')),
    path('sessions/', include('sessions.urls')),
    path('password_reset/', include('password_reset.urls')),
    path('two_factor_auth/', include('two_factor_auth.urls')),
    # Rutas para pruebas del microservicio
    # path('api/auth/', include('auth_service.api.urls')),  # Nuevas rutas para probar directamente el auth_service
    path('api/', include('auth_service.api.urls')),

]
