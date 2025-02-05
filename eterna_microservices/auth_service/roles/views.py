# roles/views.py

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Role  # Asumiendo que tienes un modelo Role

def create_role(request):
    # Lógica para crear un rol
    # Aquí, por ejemplo, podrías recibir un POST con el nombre del rol
    if request.method == "POST":
        role_name = request.POST.get('name')  # Supongamos que se pasa un parámetro 'name'
        if role_name:
            role = Role.objects.create(name=role_name)
            return JsonResponse({'message': f'Role {role.name} created successfully'}, status=201)
        return JsonResponse({'error': 'Role name is required'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_roles(request):
    # Obtener los roles del usuario autenticado
    user_roles = request.user.roles.all()
    roles_list = [{'id': role.id, 'name': role.name} for role in user_roles]
    return JsonResponse({'roles': roles_list})