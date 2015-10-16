from rest_framework import serializers
from .models import Paquete

class PaqueteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Paquete
		fields = ('nombre_paquete', 'mensualidad', 'max_locales', 'max_promo', 'max_cupones', 'have_fidelidad',)