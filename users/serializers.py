from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "address", "is_registered"]

        extra_kwargs = {
            "id": {"read_only": True},
            "is_registered": {"read_only": True},
        }
class LoginRequestSerializer(serializers.Serializer):
    token=serializers.CharField()