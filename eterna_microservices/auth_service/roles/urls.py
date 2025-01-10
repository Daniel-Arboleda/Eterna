# roles/urls.py


from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_role, name='create_role'),
    path('list/', views.list_roles, name='list_roles'),
]
