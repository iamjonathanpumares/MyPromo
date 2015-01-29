from django import forms
from .models import Promocion

class PromocionForm(forms.ModelForm):
	titulo = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))
	vigencia = forms.DateField(widget=forms.TextInput(attrs={ 'id': 'fecha'}))
	descripcion = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control'}))
	imagen = forms.ImageField(widget=forms.ClearableFileInput(attrs={ 'class': 'file', 'multiple': 'true', 'data-preview-file-type': 'any'}))

	class Meta:
		model = Promocion
		fields = ['titulo', 'vigencia', 'descripcion', 'imagen']

	def save(self, commit=True, *args, **kwargs):
		promocion = super(PromocionForm, self).save(commit=False)
		promocion.promocion_afiliado = kwargs['promocion_af']
		#usuarios_finales = User.objects.filter(gruops__name='Usuario')
		#for usuario_final in usuarios_finales:
		if commit:
			promocion.save()
		return promocion

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