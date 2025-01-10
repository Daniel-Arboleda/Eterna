# sessions/urls.py


from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='session_login'),
    path('logout/', views.logout, name='session_logout'),
]
