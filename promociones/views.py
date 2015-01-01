from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import BaseUpdateView
from userprofiles.models import Afiliado
from .models import Promocion
from .forms import PromocionForm, PromocionUpdateForm

class AfiliadoPromocionListView(ListView):
	model = Afiliado
	template_name = 'promociones_afiliados.html'

def PromocionView(request, afiliado):
	promocion_afiliado = get_object_or_404(Afiliado, user__username=afiliado)
	promociones = Promocion.objects.filter(promocion_afiliado__user__username=afiliado)
	if request.method == 'POST':
		form = PromocionForm(request.POST, request.FILES)
		if form.is_valid():
			promocion = form.save(commit=True, promocion_af=promocion_afiliado)
			messages.info(request, 'Promocion agregada') # Creamos un mensaje de exito para mostrarlo en la otra vista
			form = PromocionForm()
			return render(request, 'promociones.html', { 'promociones': promociones, 'form': form })
	else:
		form = PromocionForm()
	return render(request, 'promociones.html', { 'promociones': promociones, 'form': form })

class PromocionUpdateView(UpdateView):
	form_class = PromocionUpdateForm
	template_name = 'modificar_promocion.html'
	model = Promocion

	def form_valid(self, form):
		self.object = form.save(promocion=self.object)
		request = self.request
		messages.info(request, 'Promocion modificada')
		return super(BaseUpdateView, self).get(request)
