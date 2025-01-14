# users/urls.py


from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('user/<int:user_id>/', views.get_user, name='get_user'),
]
