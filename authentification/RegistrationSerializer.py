# myapp/serializers.py
from rest_framework import serializers

from model.models import Utilisateur


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'nom', 'prenom', 'password']

    def create(self, validated_data):
        user = Utilisateur.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            nom=validated_data['nom'],
            prenom=validated_data['prenom'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
