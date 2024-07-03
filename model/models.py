import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Vous devez entrer un nom d'utilisateur")

        user = self.model(
            username=username
            # username = self.get_by_natural_key(username)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Utilisateur(AbstractBaseUser):
    mon_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date_mise_a_jour = models.DateTimeField(verbose_name="Date de mise a jour", auto_now=True)
    username = models.CharField(
        unique=True,
        max_length=255,
        blank=False
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )
    nom = models.CharField(max_length=250, verbose_name='nom')
    prenom = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

# Create your models here.
