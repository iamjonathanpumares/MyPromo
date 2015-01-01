from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, BaseUpdateView
from userprofiles.models import Afiliado
from .models import Cupon
from .forms import CuponForm, CuponUpdateForm

class AfiliadoCuponListView(ListView):
	model = Afiliado
	template_name = 'cupones_afiliados.html'

def CuponView(request, afiliado):
	cupon_afiliado = get_object_or_404(Afiliado, user__username=afiliado)
	cupones = Cupon.objects.filter(cupon_afiliado__user__username=afiliado)
	if request.method == 'POST':
		form = CuponForm(request.POST, request.FILES)
		if form.is_valid():
			cupon = form.save(commit=True, cupon_af=cupon_afiliado)
			messages.info(request, 'Cupon agregado') # Creamos un mensaje de exito para mostrarlo en la otra vista
			form = CuponForm()
			return render(request, 'cupones.html', { 'cupones': cupones, 'form': form })
	else:
		form = CuponForm()
	return render(request, 'cupones.html', { 'cupones': cupones, 'form': form })

class CuponUpdateView(UpdateView):
	form_class = CuponUpdateForm
	template_name = 'modificar_cupon.html'
	model = Cupon

	def form_valid(self, form):
		self.object = form.save(cupon=self.object)
		request = self.request
		messages.info(request, 'Cupon modificado')
		return super(BaseUpdateView, self).get(request)
