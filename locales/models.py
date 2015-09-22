from django.db import models
from userprofiles.models import Afiliado

class Local(models.Model):
	afiliado = models.ForeignKey(Afiliado, related_name='locales')
	direccion = models.CharField(max_length=150)
	telefono = models.CharField(max_length=15, verbose_name='Telefono')
	latitud = models.FloatField()
	longitud = models.FloatField()
	estado = models.CharField('Estado', max_length=150)
	localidad = models.CharField('Localidad', max_length=150)
	is_matriz = models.BooleanField()
	imagen_local = models.ImageField(upload_to='userprofiles/locales', verbose_name='Imagen del local', blank=True, null=True)

	def __unicode__(self):
		return self.local_afiliado.user.username + " - " + self.direccion
