from rest_framework import serializers

from model.models import Utilisateur


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['username', 'password']
