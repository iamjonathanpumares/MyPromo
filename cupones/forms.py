from django import forms
from .models import Cupon
from userprofiles.models import Afiliado
from django.contrib.auth.models import User

class CuponForm(forms.ModelForm):
	titulo = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))
	fecha_inicio = forms.DateField(widget=forms.TextInput(attrs={ 'class': 'fecha'}))
	vigencia = forms.DateField(widget=forms.TextInput(attrs={ 'class': 'fecha'}))
	descripcion = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control'}))
	imagen = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={ 'class': 'file', 'multiple': 'true', 'data-preview-file-type': 'any'}))

	class Meta:
		model = Cupon
		fields = ['titulo', 'fecha_inicio', 'vigencia', 'descripcion', 'imagen']

class CuponUpdateForm(CuponForm):
	def save(self, commit=True, *args, **kwargs):
		cupon = kwargs['cupon']
		cupon.titulo = self.cleaned_data['titulo']
		cupon.vigencia = self.cleaned_data['vigencia']
		cupon.descripcion = self.cleaned_data['descripcion']
		cupon.imagen = self.cleaned_data['imagen']
		if commit:
			cupon.save()
		return cupon