import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, nom, prenom, password=None):
        if not email:
            raise ValueError("L'utilisateur doit avoir un email")
        if not username:
            raise ValueError("L'utilisateur doit avoir un nom d'utilisateur")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            nom=nom,
            prenom=prenom,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, nom, prenom, password=None):
        user = self.create_user(
            username=username,
            email=email,
            nom=nom,
            prenom=prenom,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Utilisateur(AbstractBaseUser):
    mon_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date_mise_a_jour = models.DateTimeField(verbose_name="Date de mise a jour", auto_now=True)
    username = models.CharField(unique=True, max_length=255, blank=False)
    email = models.EmailField(unique=True, max_length=255, blank=False)
    nom = models.CharField(max_length=250, verbose_name='nom')
    prenom = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    objects = MyUserManager()



    def __str__(self):
        return f"{self.nom} {self.prenom}"