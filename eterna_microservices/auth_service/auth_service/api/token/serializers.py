# auth_service/auth_service/api/token/serializers.py


# auth_service/auth_service/api/token/serializers.py
from rest_framework import serializers

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
