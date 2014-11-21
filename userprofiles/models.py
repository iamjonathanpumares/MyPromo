from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioPromotor(AbstractBaseUser):
	idUsuarioPromotor = models.IntegerField(primary_key=True)
	username = models.CharField(verbose_name='username', unique=True, max_length=100)
	nombre = models.CharField(max_length=200)
	apellidos = models.CharField(max_length=200)

	is_active = True

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['nombre', 'apellidos']

	def get_full_name(self):
		return self.nombre + " " + self.apellidos

	def get_short_name(self):
		return self.nombre

class UsuarioPromotorManager(BaseUserManager):
	def create_user(self, username, nombre, apellidos, password):
		if not username:
			raise ValueError('Necesita tener un username')


