from django.db import models
from django.conf import settings  # Para obtener el modelo de usuario

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  # Puede ser opcional

    def __str__(self):
        return self.name

class UserRole(models.Model):
    """
    Modelo intermedio que asocia un usuario con un rol específico.
    Permite que un usuario tenga múltiples roles en caso de ser necesario.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"
    