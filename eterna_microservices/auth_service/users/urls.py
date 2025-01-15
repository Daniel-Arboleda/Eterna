# users/urls.py


from django.urls import path
from . import views
from .views import RegisterView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', views.login, name='login'),
    path('account/', views.account, name='account'),             # Ruta para los datos de la cuenta (anteriormente profile)
    path('user/<int:user_id>/', views.get_user, name='get_user'),
]
