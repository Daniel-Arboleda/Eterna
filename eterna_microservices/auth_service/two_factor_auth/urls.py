# two_factor_auth/urls.py


from django.urls import path
from . import views

urlpatterns = [
    path('enable/', views.enable_2fa, name='enable_2fa'),
    path('verify/', views.verify_2fa, name='verify_2fa'),
]
