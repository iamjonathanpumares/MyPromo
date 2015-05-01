# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django_resized import ResizedImageField


class Afiliado(models.Model):
	user = models.OneToOneField(User, related_name='perfil_afiliado')
	nombreEmpresa = models.CharField(max_length=255, verbose_name='Empresa')
	representante = models.CharField(max_length=200, verbose_name='Representante')
	descripcion = models.TextField()
	direccion = models.CharField(max_length=255, verbose_name='Direccion')
	telefono = models.CharField(max_length=15, verbose_name='Telefono')
	email = models.EmailField(max_length=100, verbose_name='Email')
	facebook = models.URLField(verbose_name='Facebook', blank=True)
	twitter = models.URLField(verbose_name='Twitter', blank=True)
	web = models.URLField('Web', blank=True)
	codigoValidacion = models.CharField(max_length=100, verbose_name='Codigo validacion')
	logo = ResizedImageField(max_width=500, max_height=500, upload_to='userprofiles/logos', verbose_name='Logo')
	giro = models.CharField(max_length=100, verbose_name='Giro')
	cartel = models.ImageField(upload_to='userprofiles/carteles', verbose_name='Cartel')
	visitas = models.IntegerField('Visualizaciones del afiliado', default=0)

	def __unicode__(self):
		return self.nombreEmpresa

class Giro(models.Model):
	giro = models.CharField('Giro o actividad de la empresa', max_length=100)

	def __unicode__(self):
		return self.giro

class Promotor(models.Model):
	user = models.OneToOneField(User, related_name='perfil_promotor')

	def __unicode__(self):
		return self.user.username

class UsuarioFinal(models.Model):
	user = models.OneToOneField(User, related_name='perfil_usuariofinal')
	afiliados = models.ManyToManyField(Afiliado, through='Rating', related_name='usuarios_finales')
	full_name = models.CharField('Nombre Completo', max_length=250)

	def __unicode__(self):
		return self.user.username

class Local(models.Model):
	latitud = models.FloatField()
	longitud = models.FloatField()
	direccion = models.CharField(max_length=80)
	local_afiliado = models.ForeignKey(Afiliado, related_name='locales')

	def __unicode__(self):
		return self.local_afiliado.user.username + " - " + self.direccion

class Rating(models.Model):
	usuario_final = models.ForeignKey(UsuarioFinal)
	afiliado = models.ForeignKey(Afiliado)
	puntuacion = models.FloatField('Puntuación de cada usuario')

	def __unicode__(self):
		return self.usuario_final.user.username + " - " + self.afiliado.nombreEmpresa + ": " + str(self.puntuacion) + " votos"
