from django.urls import path
from . import views
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('account/', views.account, name='account'),
    path('user/<int:user_id>/', views.get_user, name='get_user'),
    path('roles/', views.user_roles, name='user_roles'),  # Nueva ruta para obtener roles
]
