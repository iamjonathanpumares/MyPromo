from rest_framework import serializers
from .models import Afiliado, Local, Rating, UsuarioFinal
from django.contrib.auth.models import User
from cupones.models import Cupon
from cupones.serializers import CuponSerializer
from promociones.serializers import PromocionSerializer

class RatingSerializer(serializers.ModelSerializer):
	#usuario_final = UsuarioFinalSerializer()

	class Meta:
		model = Rating
		fields = ('id', 'afiliado', 'puntuacion',)


class UsuarioFinalSerializer(serializers.ModelSerializer):
	rating_set = RatingSerializer(many=True, read_only=True)
	class Meta:
		model = UsuarioFinal
		fields = ('id', 'full_name', 'rating_set')


class AfiliadoSerializer(serializers.ModelSerializer):
	rating_set = RatingSerializer(many=True, read_only=True)

	class Meta:
		model = Afiliado
		fields = ('id', 'nombreEmpresa', 'direccion', 'telefono', 'email', 'facebook', 'twitter', 'codigoValidacion', 'logo', 'descripcion', 'giro', 'rating_set')

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

class AfiliadoCuponesPromocionesSerializer(serializers.ModelSerializer):
	#cupones_active = serializers.SerializerMethodField()
	cupones = CuponSerializer(many=True, read_only=True)
	"""cupones = serializers.HyperlinkedRelatedField(
		queryset=Cupon.objects.filter(status='Activo'),
		many=True,
		view_name='cupon_detail_api'
	)"""
	promociones = PromocionSerializer(many=True, read_only=True)
	rating_set = RatingSerializer(many=True, read_only=True)

	class Meta:
		model = Afiliado
		fields = ('id', 'nombreEmpresa', 'direccion', 'telefono', 'email', 'facebook', 'twitter', 'codigoValidacion', 'logo', 'descripcion', 'giro', 'cupones', 'promociones', 'rating_set')

	"""def get_cupones_active(self, obj, usuario):
		cupones_queryset = Cupon.objects.filter(status='Activo')
		serializer = CuponSerializer(instance=cupones_queryset, many=True)
		return serializer.data"""

class AfiliadoCartelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Afiliado
		fields = ('cartel',)

class LocalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Local
		fields = ('id', 'latitud', 'longitud', 'direccion', 'local_afiliado')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

"""class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')"""