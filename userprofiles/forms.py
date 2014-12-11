# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from .models import Afiliado

class LoginForm(AuthenticationForm):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'ID' }))
	password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'placeholder': 'Contraseña' }))

""" Gracias a la herencia en Python podemos aprovecharla para utilizar clases ya definidas y sin escribir tanto codigo, 
	Django ya trae clases para la autenticacion del usuario.
	En este caso heredamos de la clase UserCreationForm que se encuentra en django.contrib.auth.forms.UserCreationForm y
	creamos un formulario para la creacion de nuestro usuario """
class RegistrationUsuarioPromotorForm(UserCreationForm):
	username = forms.RegexField(
        regex=r'^[0-9]+$',
        error_messages={
            'invalid': ("Este campo solo puede contener numeros.")}, widget=forms.TextInput(attrs={ 'class': 'form-control'}))
	first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={ 'class': 'form-control'}))
	last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={ 'class': 'form-control'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'form-control'}), label="Password", required=True)
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'form-control'}), label="Password (again)", required=True)

	""" Como nuestra clase padre UserCreationForm hereda de forms.ModelForm, 
		que practicamente es un formulario basado en un modelo, 
		en este caso de nuestro modelo personalizado de usuario UsuarioPromotor """
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

	""" En este caso estamos usando un metodo llamado save que ya traen los formularios, 
		y que se ejecuta para guardar un objeto de tipo Modelo y guardarlo en la base de datos """
	def save(self, commit=True):
		user = super(RegistrationUsuarioPromotorForm, self).save(commit=True)
		promotor = Group.objects.get(name='Promotor')
		user.groups.add(promotor)
		if commit:
			user.save()
		return user

class AfiliadoForm(forms.ModelForm):
	class Meta:
		model = Afiliado
		fields = ['nombreEmpresa', 'representante', 'direccion', 'telefono', 'email', 'facebook', 'twitter', 'codigoValidacion', 'logo', 'giro', 'cartel']

	def guardarAfiliado(self, usuario):
		nombreEmpresa = self.cleaned_data['nombreEmpresa']
		representante = self.cleaned_data['representante']
		direccion = self.cleaned_data['direccion']
		telefono = self.cleaned_data['telefono']
		email = self.cleaned_data['email']
		facebook = self.cleaned_data['facebook']
		twitter = self.cleaned_data['twitter']
		codigoValidacion = self.cleaned_data['codigoValidacion']
		logo = self.cleaned_data['logo']
		giro = self.cleaned_data['giro']
		cartel = self.cleaned_data['cartel']
		afiliado = Afiliado(user=usuario, nombreEmpresa=nombreEmpresa, representante=representante, direccion=direccion, telefono=telefono, email=email, facebook=facebook, twitter=twitter, codigoValidacion=codigoValidacion, logo=logo, giro=giro, cartel=cartel)
		afiliado.save()
		return afiliado

	#def clean(self): # Este metodo override(sobreescrito) es el encargado de la validacion de multiples campos del formulario
		""" Llamamos a la superclase para que se ejecute el metodo clean del padre 
		        y nos devuelva un diccionario cleaned_data, 
		        con los campos del formulario ya convertidos a su tipo de dato correcto """
		#cleaned_data = super(RegistrationUsuarioPromotorForm, self).clean()

		""" Comprobamos si en el diccionario cleaned_data 
			contiene los campos del formulario password1 y password2 """
		"""if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data: 
			if self.cleaned_data['password1'] != self.cleaned_data['password2']: # Comprobamos si la contrasenas son diferentes
				raise forms.ValidationError('Las contraseñas no coinciden') # Si son diferentes lanzamos un error
			return self.cleaned_data # De lo contrario retornamos el diccionario cleaned_data"""
