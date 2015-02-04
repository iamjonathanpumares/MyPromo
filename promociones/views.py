# -*- encoding: utf-8 -*-
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
		form = PromocionForm()
	return render(request, 'promociones.html', { 'promocion_afiliado': promocion_afiliado, 'promociones': promociones })

def agregar_promocion(request, afiliado):
	afiliado = Afiliado.objects.get(user__username=afiliado)
	if request.method == 'POST':
		form = PromocionForm(request.POST, request.FILES)
		if form.is_valid():
			user_afiliado = form.save(commit=False)
			user_afiliado.promocion_afiliado = afiliado
			user_afiliado.save()
			if 'guardar-agregar' in request.POST:
				messages.info(request, 'Promoción agregada') # Creamos un mensaje de exito para mostrarlo en la otra vista
				form = PromocionForm()
				return render(request, 'agregar_promocion.html', { 'form': form })
			elif 'guardar-salir' in request.POST:
				messages.info(request, 'Promoción agregada') # Creamos un mensaje de exito para mostrarlo en la otra vista
				return redirect('/promociones/lista/%s' % afiliado.user.username)
	else:
		form = PromocionForm()
	return render(request, 'agregar_promocion.html', { 'form': form })

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
		promocion_afiliado = get_object_or_404(Afiliado, user__username=usuario)
		promociones = Promocion.objects.filter(promocion_afiliado__user__username=usuario)
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
			form = PromocionForm()
		return render(request, 'afiliado_promociones.html', { 'promocion_afiliado': promocion_afiliado, 'promociones': promociones })
	else:
		raise Http404

def agregar_promocion_afiliado(request, usuario):
	if request.user.username == usuario:
		afiliado = Afiliado.objects.get(user__username=usuario)
		if request.method == 'POST':
			form = PromocionForm(request.POST, request.FILES)
			if form.is_valid():
				user_afiliado = form.save(commit=False)
				user_afiliado.promocion_afiliado = afiliado
				user_afiliado.save()
				if 'guardar-agregar' in request.POST:
					messages.info(request, 'Promoción agregada') # Creamos un mensaje de exito para mostrarlo en la otra vista
					form = PromocionForm()
					return render(request, 'afiliado_agregar_promocion.html', { 'form': form })
				elif 'guardar-salir' in request.POST:
					messages.info(request, 'Promoción agregada') # Creamos un mensaje de exito para mostrarlo en la otra vista
					return redirect('/%s/promociones/' % afiliado.user.username)
		else:
			form = PromocionForm()
		return render(request, 'afiliado_agregar_promocion.html', { 'form': form })

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
