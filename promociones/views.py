from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import BaseUpdateView
from userprofiles.models import Afiliado
from .models import Promocion, UsuariosPromociones
from .forms import PromocionForm, PromocionUpdateForm
import json

class AfiliadoPromocionListView(ListView):
	model = Afiliado
	template_name = 'promociones_afiliados.html'

def PromocionView(request, afiliado):
	promocion_afiliado = get_object_or_404(Afiliado, user__username=afiliado)
	promociones = Promocion.objects.filter(promocion_afiliado__user__username=afiliado)
	if request.method == 'POST':
		if 'promocion_id' in request.POST:
			try:
				id_promocion = request.POST['promocion_id']
				promocion = Promocion.objects.get(pk=id_promocion)
				mensaje = { "status": "True", "promocion_id": promocion.id }
				promocion.delete()
				return HttpResponse(json.dumps(mensaje))
			except:
				mensaje = { "status": "False" }
				return HttpResponse(json.dumps(mensaje))
		else:
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

def AfiliadoPromocionView(request, usuario):
	if request.user.username == usuario:
		promocion_afiliado = get_object_or_404(Afiliado, user__username=usuario) # Usamos el shortcut get_object_or_404 para traernos el username del afiliado
		promociones = Promocion.objects.filter(promocion_afiliado__user__username=usuario)
		if request.method == 'POST': # Se comprueba si el metodo es POST
			form = PromocionForm(request.POST, request.FILES) # Creamos una instancia de promocionForm y le pasamos los datos del formulario para que los valide
			if form.is_valid(): # Si todo a salido bien y no hubo error al momento de validar los datos del formulario pasa a lo siguiente
				promocion = form.save(commit=True, promocion_af=promocion_afiliado) # Llamamos al metodo save() del form para guardar un promocion nuevo y nos retorna el objeto ya creado
				messages.info(request, 'Promocion agregada') # Creamos un mensaje de exito para mostrarlo en la otra vista
				form = PromocionForm() # Ahora instanciamos otra vez form para que me muestre el formulario
				return render(request, 'afiliado_promociones.html', { 'promociones': promociones, 'form': form }) # Renderizamos la plantilla junto con su contexto
		else:
			form = PromocionForm()
		return render(request, 'afiliado_promociones.html', { 'promociones': promociones, 'form': form })
	else:
		raise Http404

# Django REST Framework -----------------------------------------------------------------------------------------------------------------

from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PromocionSerializer

class PromocionAPIView(generics.ListAPIView):
	queryset = Promocion.objects.all()
	serializer_class = PromocionSerializer

class PromocionAfiliadoAPIView(generics.ListAPIView):
	serializer_class = PromocionSerializer

	"""
		Sobreescribimos el metodo get_queryset, para que nos devuelva
		una consulta, que seran los cupones de cada afiliado.
	"""
	def get_queryset(self):
		promocion_afiliado = self.kwargs['promocion_afiliado'] # Desde la URL por medio de los kwargs le pasamos el id del afiliado
		return Promocion.objects.filter(promocion_afiliado=promocion_afiliado) # Retorna un tipo de dato queryset para mostrarse en la vista

@api_view(['POST'])
def UsuariosPromocionesAgregar(request):
	if request.method == 'POST':
		#data = JSONParser().parse(request)
		data = request.data
		id_usuario = data['id_usuario']
		id_promocion = data['id_promocion']
		respuesta = {}
		try:
			usuario = User.objects.get(username=id_usuario)
		except User.DoesNotExist:
			respuesta['estado'] = "False"
			return Response(respuesta)
		else:
			try:
				promocion = Promocion.objects.get(id=id_promocion)
			except Promocion.DoesNotExist:
				respuesta['estado'] = "False"
				return Response(respuesta)
			else:
				UsuariosPromociones.objects.create(usuario=usuario, promocion=promocion)
				respuesta['estado'] = "True"
				return Response(respuesta)
