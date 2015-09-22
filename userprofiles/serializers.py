# -*- encoding: utf-8 -*-
from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from cupones.models import Cupon
from cupones.serializers import CuponSerializer
from promociones.serializers import PromocionSerializer
from promociones.models import Promocion
from locales.models import Local

from .models import Afiliado, Rating, UsuarioFinal, Giro

UserModel = get_user_model()

class GiroSerializer(serializers.ModelSerializer):
	class Meta:
		model = Giro
		fields = ('id', 'giro',)

class RatingAfiliadoSerializer(serializers.ModelSerializer):
	#usuario_final = UsuarioFinalSerializer()

	class Meta:
		model = Rating
		fields = ('id', 'afiliado', 'puntuacion',)

class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class UsuarioFinalRatingSerializer(serializers.ModelSerializer):
	user = UserRatingSerializer()
	class Meta:
		model = UsuarioFinal
		fields = ('user',)       

class RatingUsuarioFinalSerializer(serializers.ModelSerializer):
	usuario_final = UsuarioFinalRatingSerializer()

	class Meta:
		model = Rating
		fields = ('id', 'usuario_final', 'puntuacion',)

class UsuarioFinalSerializer(serializers.ModelSerializer):
	rating_set = RatingAfiliadoSerializer(many=True, read_only=True)
	class Meta:
		model = UsuarioFinal
		fields = ('id', 'full_name', 'rating_set')


class AfiliadoSerializer(serializers.ModelSerializer):
	rating_set = RatingUsuarioFinalSerializer(many=True, read_only=True)

	class Meta:
		model = Afiliado
		fields = ('id', 'nombreEmpresa', 'direccion', 'telefono', 'email', 'facebook', 'twitter', 'web', 'codigoValidacion', 'logo', 'descripcion', 'giro', 'visitas', 'rating_set',)

class AfiliadoCuponesSerializer(serializers.ModelSerializer):
	cupones = CuponSerializer(many=True, read_only=True) 

	class Meta:
		model = Afiliado
		fields = ('id', 'nombreEmpresa', 'direccion', 'telefono', 'email', 'facebook', 'twitter', 'codigoValidacion', 'logo', 'descripcion', 'giro', 'cupones')

class AfiliadoPromocionesSerializer(serializers.ModelSerializer):
	rating_set = RatingUsuarioFinalSerializer(many=True, read_only=True)
	promociones = PromocionSerializer(many=True, read_only=True)

	class Meta:
		model = Afiliado
		fields = ('id', 'nombreEmpresa', 'direccion', 'telefono', 'email', 'facebook', 'twitter', 'web', 'codigoValidacion', 'logo', 'descripcion', 'giro', 'visitas', 'promociones', 'rating_set')


#class AfiliadoCuponesPromocionesSerializer(serializers.ModelSerializer):
	#cupones_active = serializers.SerializerMethodField()
	#cupones = CuponSerializer(many=True, read_only=True)
	"""cupones = serializers.HyperlinkedRelatedField(
		queryset=Cupon.objects.filter(status='Activo'),
		many=True,
		view_name='cupon_detail_api'
	)"""
	#promociones = PromocionSerializer(many=True, read_only=True)
	#rating_set = RatingSerializer(many=True, read_only=True)

	#class Meta:
		#model = Afiliado
		#fields = ('id', 'nombreEmpresa', 'direccion', 'telefono', 'email', 'facebook', 'twitter', 'codigoValidacion', 'logo', 'descripcion', 'giro', 'cupones', 'promociones', 'rating_set')

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

class ConteoGeneralSerializer(serializers.Serializer):
	numero_afiliados = serializers.IntegerField()
	numero_cupones = serializers.IntegerField()
	numero_promociones = serializers.IntegerField()

class SignupSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField(min_length=8)
	confirm_password = serializers.CharField(min_length=8)
	email = serializers.EmailField()

	def validate_username(self, value):
		no_users = UserModel.objects.filter(username=value).count()
		if no_users != 0:
			raise serializers.ValidationError('Ya existe ese nombre de usuario registradop')
		return value

	def validate_email(self, value):
		no_users = UserModel.objects.filter(email=value).count()
		if no_users != 0:
			raise serializers.ValidationError('Ya existe un usuario registrado con ese email')
		return value


	def validate(self, data):
		if data['password'] != data['confirm_password']:
			raise serializers.ValidationError('Las contraseñas no coinciden')
		return data

"""class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')"""