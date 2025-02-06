from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import uuid

User = get_user_model()

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="password_reset_tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def is_expired(self):
        """Verifica si el token ya expiró"""
        return now() > self.expires_at

    def mark_as_used(self):
        """Marca el token como usado"""
        self.used = True
        self.save()