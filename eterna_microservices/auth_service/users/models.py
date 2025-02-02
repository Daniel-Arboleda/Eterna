from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from roles.models import Role  # Importar roles

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, roles=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Si no se proporcionan roles, asignar el rol por defecto "Cliente"
        if not roles:
            roles = [Role.objects.get(name="Cliente")]
        
        user.roles.set(roles)  # Asignar los roles al usuario
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        superadmin_role = Role.objects.get(name="Superadministrador")
        return self.create_user(email, password, roles=[superadmin_role], **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role, related_name="users")  # Relación de muchos a muchos con los roles

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
