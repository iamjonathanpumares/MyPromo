from rest_framework import serializers
from .models import Cupon

class CuponSerializer(serializers.ModelSerializer):
	queryset = Cupon.objects.filter(status='Activo')
	class Meta:
		model = Cupon
		fields = ('id', 'titulo', 'fecha_creacion', 'vigencia', 'descripcion', 'imagen', 'cupon_afiliado')