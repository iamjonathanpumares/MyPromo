# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, BaseUpdateView
from userprofiles.mixins import LoginRequiredMixin
from userprofiles.models import Afiliado
from .models import Cupon, UsuariosCupones
from .forms import CuponForm, CuponUpdateForm
import json

class AfiliadoCuponListView(LoginRequiredMixin, ListView): # Vista que hereda de ListView para mostrar la lista de afiliados
	model = Afiliado # Especificamos el modelo para traernos todos los objetos y mostrar la lista
	template_name = 'cupones_afiliados.html' # Template que sera renderizado para mostrar la lista de afiliados

def CuponView(request, afiliado): # Vista de funcion donde se guardara un nuevo cupon y se mostrara la lista de cupones del afiliado
	cupon_afiliado = get_object_or_404(Afiliado, user__username=afiliado) # Usamos el shortcut get_object_or_404 para traernos el username del afiliado
	cupones = Cupon.objects.filter(cupon_afiliado__user__username=afiliado) # Una consulta que retorna todos los cupones de dicho afiliado que se tomo en el parametro afiliado
	if request.method == 'POST': # Se comprueba si el metodo es POST
		if 'cupon_id' in request.POST:
			try:
				id_cupon = request.POST['cupon_id']
				cupon = Cupon.objects.get(pk=id_cupon)
				mensaje = { "status": "True", "cupon_id": cupon.id }
				cupon.delete()
				return HttpResponse(json.dumps(mensaje))
			except:
				mensaje = { "status": "False" }
				return HttpResponse(json.dumps(mensaje))
		else:
			form = CuponForm(request.POST, request.FILES) # Creamos una instancia de CuponForm y le pasamos los datos del formulario para que los valide
			if form.is_valid(): # Si todo a salido bien y no hubo error al momento de validar los datos del formulario pasa a lo siguiente
				cupon = form.save(commit=True, cupon_af=cupon_afiliado) # Llamamos al metodo save() del form para guardar un cupon nuevo y nos retorna el objeto ya creado
				messages.info(request, 'Cupon agregado') # Creamos un mensaje de exito para mostrarlo en la otra vista
				form = CuponForm() # Ahora instanciamos otra vez form para que me muestre el formulario
				return render(request, 'cupones.html', { 'cupones': cupones, 'form': form }) # Renderizamos la plantilla junto con su contexto
	else:
		form = CuponForm()
	return render(request, 'cupones.html', { 'cupones': cupones, 'form': form })

class CuponUpdateView(UpdateView): # Vista que hereda de UpdateView para actualizar un objeto ya creado
	form_class = CuponUpdateForm # Especificamos el formulario a usar
	template_name = 'modificar_cupon.html' # Especificamos la plantilla a renderizar
	model = Cupon # Especificamos el modelo en donde buscara el objeto a actualizar

	def form_valid(self, form): # Sobreescribimos el metodo form_valid para cambiar su comportamiento
		self.object = form.save(cupon=self.object) # Actualizamos el objeto con sus cambios y retorna ese mismo objeto
		request = self.request # Asignamos a una variable local el self.request
		messages.info(request, 'Cupon modificado') # Mandamos un mensaje de informacion especificando que se ha modificado el cupon
		return super(BaseUpdateView, self).get(request) # Mandamos a llamar al padre de get para que renderize de vuelta el formulario

def AfiliadoCuponView(request, usuario):
	if request.user.username == usuario:
		cupon_afiliado = get_object_or_404(Afiliado, user__username=usuario) # Usamos el shortcut get_object_or_404 para traernos el username del afiliado
		cupones = Cupon.objects.filter(cupon_afiliado__user__username=usuario)
		if request.method == 'POST': # Se comprueba si el metodo es POST
			form = CuponForm(request.POST, request.FILES) # Creamos una instancia de CuponForm y le pasamos los datos del formulario para que los valide
			if form.is_valid(): # Si todo a salido bien y no hubo error al momento de validar los datos del formulario pasa a lo siguiente
				cupon = form.save(commit=True, cupon_af=cupon_afiliado) # Llamamos al metodo save() del form para guardar un cupon nuevo y nos retorna el objeto ya creado
				messages.info(request, 'Cupon agregado') # Creamos un mensaje de exito para mostrarlo en la otra vista
				form = CuponForm() # Ahora instanciamos otra vez form para que me muestre el formulario
				return render(request, 'afiliado_cupones.html', { 'cupones': cupones, 'form': form }) # Renderizamos la plantilla junto con su contexto
		else:
			form = CuponForm()
		return render(request, 'afiliado_cupones.html', { 'cupones': cupones, 'form': form })
	else:
		raise Http404

# Django REST Framework -----------------------------------------------------------------------------------------------------------------

from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CuponSerializer

class CuponAPIView(generics.ListAPIView):
	queryset = Cupon.objects.filter(status='Activo')
	serializer_class = CuponSerializer

class CuponAfiliadoAPIView(generics.ListAPIView):
	serializer_class = CuponSerializer

	"""
		Sobreescribimos el metodo get_queryset, para que nos devuelva
		una consulta, que seran los cupones de cada afiliado.
	"""
	def get_queryset(self):
		cupon_afiliado = self.kwargs['cupon_afiliado'] # Desde la URL por medio de los kwargs le pasamos el id del afiliado
		return Cupon.objects.filter(cupon_afiliado=cupon_afiliado) # Retorna un tipo de dato queryset para mostrarse en la vista

class UsuariosCuponesDisponibles(APIView):
	def get(self, request, usuario, format=None):
		cupones = Cupon.objects.exclude(users__username=usuario).filter(status='Activo')
		serializer = CuponSerializer(cupones, many=True)
		return Response(serializer.data)

@api_view(['POST'])
def UsuariosCuponesAgregar(request):
	if request.method == 'POST':
		#data = JSONParser().parse(request)
		data = request.data
		id_usuario = data['id_usuario']
		id_cupon = data['id_cupon']
		respuesta = {}
		try:
			usuario = User.objects.get(username=id_usuario)
		except User.DoesNotExist:
			respuesta['estado'] = "False"
			return Response(respuesta)
		else:
			try:
				cupon = Cupon.objects.get(id=id_cupon)
			except Cupon.DoesNotExist:
				respuesta['estado'] = "False"
				return Response(respuesta)
			else:
				UsuariosCupones.objects.create(usuario=usuario, cupon_usuario=cupon)
				respuesta['estado'] = "True"
				return Response(respuesta)


