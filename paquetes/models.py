# -*- coding: utf-8 -*-
from django.db import models

class Paquete(models.Model):
	nombre_paquete = models.CharField('Nombre del paquete', max_length=50)
	mensualidad = models.FloatField('Mensualidad')
	max_locales = models.PositiveSmallIntegerField('Máximo de locales por afiliado')
	max_promo = models.PositiveSmallIntegerField('Máximo de promociones por afiliado')
	max_cupones = models.PositiveSmallIntegerField('Máximo de cupones por afiliado')
	have_fidelidad = models.BooleanField('Tiene fidelidad')
