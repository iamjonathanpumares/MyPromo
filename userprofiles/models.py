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

	def __unicode__(self):
		return self.username

	def get_full_name(self):
		return self.nombre + " " + self.apellidos

	def get_short_name(self):
		return self.nombre

class UsuarioPromotorManager(BaseUserManager):
	def create_user(self, username, nombre, apellidos, password):
		if not username:
			raise ValueError('Necesita tener un username')

		user = self.model(
			username=username,
			nombre=nombre,
			apellidos=apellidos
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

class UsuarioAfiliado(AbstractBaseUser):
	idUsuarioAfiliado = models.IntegerField(primary_key=True)
	username = models.CharField(verbose_name='username', unique=True, max_length=100)
	nombreEmpresa = models.CharField(max_length=255)
	representante = models.CharField(max_length=200)
	direccion = models.CharField(max_length=255)
	telefono = models.CharField(max_length=15)
	email = models.EmailField(max_length=100)
	facebook = models.CharField(max_length=200)
	twitter = models.CharField(max_length=100)
	codigoValidacion = models.CharField(max_length=255)
	logo = models.ImageField(upload_to='logos')
	giro = models.CharField(max_length=100)
	cartel = models.ImageField(upload_to='carteles')

	is_active = True

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['nombreEmpresa', 'representante', 'direccion, telefono', 'email', 'facebook', 'twitter', 'codigoValidacion', 'logo', 'giro', 'cartel']

	def __unicode__(self):
		self.username

	def get_full_name(self):
		return self.nombreEmpresa + " " + self.representante

	def get_short_name(self):
		return self.nombreEmpresa

class UsuarioAfiliadoManager(BaseUserManager):
	def create_user(self, username, nombreEmpresa, representante, direccion, telefono, email, facebook, twitter, codigoValidacion, logo, giro, cartel, password):
		if not username:
			raise ValueError('Necesita tener un username')

		user = self.model(
			username=username,
			nombreEmpresa=nombreEmpresa,
			representante=representante,
			direccion=direccion,
			telefono=telefono,
			email=email,
			facebook=facebook,
			twitter=twitter,
			codigoValidacion=codigoValidacion,
			logo=logo,
			giro=giro,
			cartel=cartel 
		)
		user.set_password(password)
		user.save(using=self._db)
		return user
