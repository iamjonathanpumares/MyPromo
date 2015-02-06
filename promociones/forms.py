from django import forms
from .models import Promocion

class PromocionForm(forms.ModelForm):
	titulo = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))
	vigencia = forms.DateField(widget=forms.TextInput(attrs={ 'id': 'fecha'}))
	descripcion = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control'}))
	imagen = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={ 'class': 'file', 'multiple': 'true', 'data-preview-file-type': 'any'}))

	class Meta:
		model = Promocion
		fields = ['titulo', 'vigencia', 'descripcion', 'imagen']

class PromocionUpdateForm(PromocionForm):
	def save(self, commit=True, *args, **kwargs):
		promocion = kwargs['promocion']
		promocion.titulo = self.cleaned_data['titulo']
		promocion.vigencia = self.cleaned_data['vigencia']
		promocion.descripcion = self.cleaned_data['descripcion']
		promocion.imagen = self.cleaned_data['imagen']
		if commit:
			promocion.save()
		return promocion