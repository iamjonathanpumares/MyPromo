from django.db import models
from django.contrib.auth.models import User
from userprofiles.models import Afiliado

class Promocion(models.Model):
	titulo = models.CharField(max_length=60)
	users = models.ManyToManyField(User, through='UsuariosPromociones')
	fecha_creacion = models.DateField(auto_now=True)
	vigencia = models.DateField()
	descripcion = models.TextField()
	status = models.CharField(max_length=10)
	imagen = models.ImageField(upload_to='promociones/imagenes')
	promocion_afiliado = models.ForeignKey(Afiliado, related_name='promociones')

	def __unicode__(self):
		return self.titulo

class UsuariosPromociones(models.Model):
	usuario = models.ForeignKey(User)
	promocion = models.ForeignKey(Promocion)
	fecha = models.DateField()

	def __unicode__(self):
		return "%s - %s" % (self.usuario.username, self.promocion.titulo)
