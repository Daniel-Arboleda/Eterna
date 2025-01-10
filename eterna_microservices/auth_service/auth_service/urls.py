# auth_service/urls.py


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('roles/', include('roles.urls')),
    path('sessions/', include('sessions.urls')),
    path('password_reset/', include('password_reset.urls')),
    path('two_factor_auth/', include('two_factor_auth.urls')),
]
