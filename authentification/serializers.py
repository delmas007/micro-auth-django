from rest_framework import serializers

from model.models import Utilisateur


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
