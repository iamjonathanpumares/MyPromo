from django.db import models
from django.contrib.auth.models import User

class Afiliado(models.Model):
	user = models.OneToOneField(User)
	nombreEmpresa = models.CharField(max_length=255, verbose_name='Empresa')
	representante = models.CharField(max_length=200, verbose_name='Representante')
	direccion = models.CharField(max_length=255, verbose_name='Direccion')
	telefono = models.CharField(max_length=15, verbose_name='Telefono')
	email = models.EmailField(max_length=100, verbose_name='Email')
	facebook = models.CharField(max_length=200, verbose_name='Facebook')
	twitter = models.CharField(max_length=100, verbose_name='Twitter')
	codigoValidacion = models.CharField(max_length=255, verbose_name='Codigo validacion')
	logo = models.ImageField(upload_to='userprofiles/logos', verbose_name='Logo')
	giro = models.CharField(max_length=100, verbose_name='Giro')
	cartel = models.ImageField(upload_to='userprofiles/carteles', verbose_name='Cartel')

	def __unicode__(self):
		return self.nombreEmpresa

class Local(models.Model):
	latitud = models.FloatField()
	longitud = models.FloatField()
	direccion = models.CharField(max_length=80)
	local_afiliado = models.ForeignKey(Afiliado)