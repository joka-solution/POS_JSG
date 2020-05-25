from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    is_vendedor = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_gerente = models.BooleanField(default=False)
    is_patron = models.BooleanField(default=False)

    def get_vendedor_profile(self):
        vendedor_profile = None
        if hasattr(self, 'vendedorprofile'):
            vendedor_profile = self.vendedorprofile
        return vendedor_profile

    def get_supervisor_profile(self):
        supervisor_profile = None
        if hasattr(self, 'supervisorprofile'):
            supervisor_profile = self.supervisorprofile
        return supervisor_profile

    def get_gerente_profile(self):
        gerente_profile = None
        if hasattr(self, 'gerenteprofile'):
            gerente_profile = self.gerenteprofile
        return gerente_profile

    def get_patron_profile(self):
        patron_profile = None
        if hasattr(self, 'patronprofile'):
            patron_profile = self.patronprofile
        return  patron_profile

    class Meta:
        db_table = 'auth_user'

class supervisorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)

class vendedorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)

class gerenteProfile(models.Model)    :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)

class patronProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)