# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import Cupon

class CuponSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cupon
		fields = ('id', 'titulo', 'fecha_creacion', 'vigencia', 'descripcion', 'status', 'imagen', 'cupon_afiliado')

class CuponesDisponiblesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cupon
		fields = ('id', 'titulo', 'fecha_creacion', 'vigencia', 'descripcion', 'imagen', 'cupon_afiliado')

class NumeroCuponesSerializer(serializers.ModelSerializer):
	numero_cupones = Cupon.objects.all().count()
	class Meta:
		model = Cupon
		fields = ('numero_cupones',)