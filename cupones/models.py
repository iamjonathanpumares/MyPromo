from django.db import models
from django.contrib.auth.models import User
from userprofiles.models import Afiliado

class Cupon(models.Model):
	titulo = models.CharField(max_length=40)
	users = models.ManyToManyField(User, through='UsuariosCupones')
	fecha_creacion = models.DateField(auto_now=True)
	vigencia = models.DateField()
	descripcion = models.TextField()
	imagen = models.ImageField(upload_to='cupones/imagenes')
	cupon_afiliado = models.ForeignKey(Afiliado, related_name='cupones')

	def __unicode__(self):
		return self.titulo

class UsuariosCupones(models.Model):
	usuario = models.ForeignKey(User)
	cupon_usuario = models.ForeignKey(Cupon)
	status = models.CharField(max_length=10)
	fecha = models.DateField()

	def __unicode__(self):
		return "%s - %s" % (self.usuario.username, self.cupon_usuario.titulo)
