from rest_framework import serializers
from .models import Promocion

class PromocionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Promocion
		fields = ('titulo', 'fecha_creacion', 'vigencia', 'descripcion', 'imagen', 'promocion_afiliado')