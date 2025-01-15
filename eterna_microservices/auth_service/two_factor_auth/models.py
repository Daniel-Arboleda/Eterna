# two_factor_auth/models.py

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class TwoFactorAuth(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=255, blank=True, null=True)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"2FA for {self.user.username}"

    def generate_secret_key(self):
        import pyotp
        self.secret_key = pyotp.random_base32()
        self.save()

    def verify_code(self, code):
        import pyotp
        totp = pyotp.TOTP(self.secret_key)
        return totp.verify(code)
