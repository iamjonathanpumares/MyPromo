from rest_framework import serializers
from .models import Afiliado, Local
from django.contrib.auth.models import User, Group
from cupones.models import Cupon
from cupones.serializers import CuponSerializer
from promociones.serializers import PromocionSerializer

class AfiliadoSerializer(serializers.ModelSerializer):

	class Meta:
		model = Afiliado
		fields = ('id', 'nombreEmpresa', 'direccion', 'telefono', 'email', 'facebook', 'twitter', 'logo', 'descripcion', 'giro')

class AfiliadoCuponesSerializer(serializers.ModelSerializer):
	cupones = CuponSerializer(many=True, read_only=True)

	class Meta:
		model = Afiliado
		fields = ('id', 'nombreEmpresa', 'direccion', 'telefono', 'email', 'facebook', 'twitter', 'codigoValidacion', 'logo', 'descripcion', 'giro', 'cupones')

class AfiliadoPromocionesSerializer(serializers.ModelSerializer):
	promociones = PromocionSerializer(many=True, read_only=True)

	class Meta:
		model = Afiliado
		fields = ('id', 'nombreEmpresa', 'direccion', 'telefono', 'email', 'facebook', 'twitter', 'codigoValidacion', 'logo', 'descripcion', 'giro', 'promociones')

class LocalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Local
		fields = ('id', 'latitud', 'longitud', 'direccion', 'local_afiliado')

"""class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')"""