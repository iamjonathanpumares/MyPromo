# -*- encoding: utf-8 -*-
from django import forms
from .models import UsuarioPromotor, UsuarioAfiliado

class RegistrationUsuarioPromotorForm(forms.ModelForm):
	username = forms.CharField(max_length=100, required=True)
	nombre = forms.CharField(max_length=200, required=True)
	apellidos = forms.CharField(max_length=200, required=True)
	password1 = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)
	password2 = forms.CharField(widget=forms.PasswordInput, label="Password (again)", required=True)

	class Meta:
		model = UsuarioPromotor
		fields = ['username', 'nombre', 'apellidos', 'password1', 'password2']

	def clean(self): # Este metodo override(sobreescrito) es el encargado de la validacion de multiples campos del formulario
		""" Llamamos a la superclase para que se ejecute el metodo clean del padre 
		        y nos devuelva un diccionario cleaned_data, 
		        con los campos del formulario ya convertidos a su tipo de dato correcto """
		cleaned_data = super(RegistrationUsuarioPromotorForm, self).clean()

		""" Comprobamos si en el diccionario cleaned_data 
			contiene los campos del formulario password1 y password2 """
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data: 
			if self.cleaned_data['password1'] != self.cleaned_data['password2']: # Comprobamos si la contrasenas son diferentes
				raise forms.ValidationError('Las contraseñas no coinciden') # Si son diferentes lanzamos un error
			return self.cleaned_data # De lo contrario retornamos el diccionario cleaned_data

	def save(self, commit=True):
		user = super(RegistrationUsuarioPromotorForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user
