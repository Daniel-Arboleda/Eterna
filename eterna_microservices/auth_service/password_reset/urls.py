# password_reset/urls.py


from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.request_reset, name='password_reset_request'),
    path('confirm/', views.confirm_reset, name='password_reset_confirm'),
]
