# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import Cupon

class CuponSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cupon
		fields = ('id', 'titulo', 'fecha_creacion', 'vigencia', 'descripcion', 'imagen', 'cupon_afiliado')