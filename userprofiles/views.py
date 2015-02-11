# -*- encoding: utf-8 -*-
import json
from cupones.models import Cupon
from promociones.models import Promocion
from django.db.models import Count, Q
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.views.generic import ListView, FormView, UpdateView
from django.views.generic.edit import BaseUpdateView
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout
from .forms import LoginForm, UserAfiliadoForm, UserAfiliadoUpdateForm, PerfilAfiliadoForm, PerfilAfiliadoUpdateForm, UsuarioCSVForm, LocalForm, RegistrationUsuarioPromotorForm, RegistrationUsuarioFinalForm, StatusUpdateForm
from .decorators import redirect_home
from .mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Afiliado, Local, UsuarioFinal, Promotor
from .load_data import importarCSV

# Login ----------------------------------------------------------------------------------------------------
class LoginUserPromotorView(FormView):
	#model = UsuarioPromotor
	template_name = 'login.html'
	success_url = '/home/'
	form_class = LoginForm

	def form_valid(self, form):
		login(self.request, form.user_cache)
		return super(LoginUserPromotorView, self).form_valid(form)

# Logout -----------------------------------------------------------------------------------------------------
def logout_view(request):
	logout(request)
	return redirect('/login/')

# Home -------------------------------------------------------------------------------------------------------
@redirect_home
def home(request):
	promocion_popular = Promocion.objects.annotate(Count('users')).order_by('users__count').reverse()[:1]
	cupon_popular = Cupon.objects.annotate(Count('users')).order_by('users__count').reverse()[:1]
	cupones_totales = Cupon.objects.all().count()
	promociones_totales = Promocion.objects.count()
	num_afiliados = Afiliado.objects.all().count()
	num_usuarios = UsuarioFinal.objects.all().count()
	return render(request, 'home.html', { 'promocion_popular': promocion_popular, 'cupon_popular': cupon_popular, 'cupones_totales': cupones_totales, 'promociones_totales': promociones_totales, 'num_afiliados': num_afiliados, 'num_usuarios': num_usuarios })

@login_required(login_url='/login/')
def home_afiliado(request, usuario):
	afiliado = get_object_or_404(Afiliado, user__username=usuario)
	promocion_popular = Promocion.objects.filter(promocion_afiliado__user__username=request.user.username).annotate(Count('users')).order_by('users__count').reverse()[:1]
	cupon_popular = Cupon.objects.filter(cupon_afiliado__user__username=request.user.username).annotate(Count('users')).order_by('users__count').reverse()[:1]
	cupones_totales = Cupon.objects.filter(cupon_afiliado__user__username=request.user.username).count()
	promociones_totales = Promocion.objects.filter(promocion_afiliado__user__username=request.user.username).count()
	num_afiliados = Afiliado.objects.all().count()
	num_usuarios = UsuarioFinal.objects.all().count()
	return render(request, 'home_afiliado.html', { 'promocion_popular': promocion_popular, 'cupon_popular': cupon_popular, 'cupones_totales': cupones_totales, 'promociones_totales': promociones_totales, 'num_afiliados': num_afiliados, 'num_usuarios': num_usuarios })



# Views Afiliado ---------------------------------------------------------------------------------------------
class AfiliadoListView(LoginRequiredMixin, ListView):
	queryset = Afiliado.objects.all()
	template_name = 'lista_empresas.html'

	def get_queryset(self):
		try:
		    name = self.request.GET.get('q', '')
		except:
		    name = ''
		if (name != ''):
		    object_list = Afiliado.objects.filter(nombreEmpresa__icontains=name)
		    self.paginate_by = None
		else:
		    object_list = Afiliado.objects.all().order_by('nombreEmpresa')
		    self.paginate_by = 15
		return object_list

	def get_context_data(self, **kwargs):
		context = super(AfiliadoListView, self).get_context_data(**kwargs)
		context['q'] = self.request.GET.get('q', '')
		return context

@permission_required('userprofiles.add_afiliado', login_url='/login/')
@login_required(login_url='/login/')
def AfiliadoView(request):
	if request.method == 'POST': # Verifica si la peticion hecha por el usuario es POST
		form_user = UserAfiliadoForm(request.POST) # Se crea una instancia del formulario UserAfiliadoForm y le pasamos los datos del formulario
		form_afiliado = PerfilAfiliadoForm(request.POST, request.FILES) # Se crea una instancia del formulario PerfilAfiliadoForm y le pasamos los datos junto con los archivo subidos
		if form_user.is_valid() and form_afiliado.is_valid(): # Verificamos si los formularios pasaron todas sus validaciones
			usuario = form_user.save() # Se crea el usuario
			afiliado = form_afiliado.save(commit=True, afiliado=usuario) # Se manda a llamar a un metodo declarado en el formulario para que guarda al afiliado
			if 'submit-guardar-salir' in request.POST:
				messages.info(request, 'Afiliado %s agregado' % form_afiliado.cleaned_data['nombreEmpresa'])
				return redirect('/lista-afiliados/')
			elif 'submit-guardar-locales' in request.POST:
				return redirect('/agregar-locales/' + form_user.cleaned_data['username'] + '/' + str(usuario.id) + '/')
	else:
		form_user = UserAfiliadoForm()
		form_afiliado = PerfilAfiliadoForm()
	return render_to_response('afiliados_agregar.html', { 'form_user': form_user, 'form_afiliado': form_afiliado }, context_instance=RequestContext(request))

def AfiliadoUpdateView(request, usuario, id): # Vista que hereda de UpdateView para actualizar un objeto ya creado
	user_afiliado = get_object_or_404(User, username=usuario)
	afiliado = get_object_or_404(Afiliado, id=id)
	if request.method == 'POST':
		form_user = UserAfiliadoUpdateForm(request.POST, instance=user_afiliado)
		form_afiliado = PerfilAfiliadoUpdateForm(request.POST, request.FILES, instance=afiliado)
		if form_user.is_valid() and form_afiliado.is_valid():
			form_user.save()
			form_afiliado.save()
			messages.info(request, 'Afiliado %s modificado' % afiliado) # Creamos un mensaje de exito para mostrarlo en la otra vista
			return redirect('/lista-afiliados/')

	else:
		if afiliado.facebook != '':
			datos = afiliado.facebook.split('.com/')
			afiliado.facebook = datos[1]
		if afiliado.twitter != '':
			datos = afiliado.twitter.split('.com/')
			afiliado.twitter = datos[1]
		form_user = UserAfiliadoUpdateForm(instance=user_afiliado)
		form_afiliado = PerfilAfiliadoUpdateForm(instance=afiliado)
	return render(request, 'modificar_afiliado.html', { 'form_user': form_user, 'form_afiliado': form_afiliado })

@permission_required('userprofiles.add_local', login_url='/login/')
@login_required(login_url='/login/')
def LocalView(request, usuario, id_usuario):
	if request.method == 'POST':
		json_locales = request.read()
		locales = json.loads(json_locales)
		usuario_afiliado = Afiliado.objects.get(user=id_usuario)
		if usuario_afiliado.user.username == usuario:
			i = 0
			num_locales = len(locales['direcciones'])
			while i < num_locales:
				local_afiliado = Local(direccion=locales['direcciones'][i], latitud=locales['latitudes'][i], longitud=locales['longitudes'][i], local_afiliado=usuario_afiliado)
				local_afiliado.save()
				i += 1
			messages.info(request, 'Locales agregados correctamente') # Creamos un mensaje de exito para mostrarlo en la otra vista
			return HttpResponse('/lista-afiliados/')
	else:
		usuario_afiliado = get_object_or_404(Afiliado, user__username=usuario, user__id=id_usuario)
	return render_to_response('locales.html', {}, context_instance=RequestContext(request))

@permission_required('userprofiles.add_local', login_url='/login/')
@login_required(login_url='/login/')
def LocalUpdateView(request, usuario, id):
	afiliado = get_object_or_404(Afiliado, user__username=usuario, id=id)
	locales = afiliado.locales.all()
	if request.method == 'POST':
		json_locales = request.read()
		locales = json.loads(json_locales)
		if afiliado.user.username == usuario:
			i = 0
			num_locales = len(locales['direcciones'])
			while i < num_locales:
				local_afiliado = Local(direccion=locales['direcciones'][i], latitud=locales['latitudes'][i], longitud=locales['longitudes'][i], local_afiliado=afiliado)
				local_afiliado.save()
				i += 1
			messages.info(request, 'Locales agregados correctamente') # Creamos un mensaje de exito para mostrarlo en la otra vista
			return HttpResponse('/lista-afiliados/')
	return render_to_response('modificar_locales.html', { 'locales': locales }, context_instance=RequestContext(request))

class StatusUpdateView(UpdateView): # Vista que hereda de UpdateView para actualizar un objeto ya creado
	form_class = StatusUpdateForm # Especificamos el formulario a usar
	template_name = 'modificar_status.html' # Especificamos la plantilla a renderizar
	model = User # Especificamos el modelo en donde buscara el objeto a actualizar
	#success_url = '/lista-afiliados/'

	def form_valid(self, form): # Sobreescribimos el metodo form_valid para cambiar su comportamiento
		self.object = form.save() # Actualizamos el objeto con sus cambios y retorna ese mismo objeto
		request = self.request # Asignamos a una variable local el self.request
		messages.info(request, 'Status modificado') # Mandamos un mensaje de informacion especificando que se ha modificado el cupon
		return super(StatusUpdateView, self).get(request) # Mandamos a llamar al padre de get para que renderize de vuelta el formulario

class UsuarioPromotorListView(ListView):
	model = User
	template_name = 'lista_usuarios.html'

class UsuarioFinalListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission = 'auth.change_user'
	#queryset = UsuarioFinal.objects.order_by('user__last_name')
	template_name = 'lista_usuarios.html'
	#paginate_by = 5

	def get_queryset(self):
		try:
		    name = self.request.GET.get('q', '')
		except:
		    name = ''
		if (name != ''):
		    object_list = UsuarioFinal.objects.filter(Q(user__username__icontains=name) | Q(user__last_name__icontains=name) | Q(user__first_name__icontains=name) | Q(user__email__icontains=name))
		    self.paginate_by = None
		else:
		    object_list = UsuarioFinal.objects.all().order_by('user__last_name')
		    self.paginate_by = 15
		return object_list

	def post(self, request, *args, **kwargs):
		if 'usuario_id' in request.POST:
			try:
				id_usuario = request.POST['usuario_id']
				usuario = UsuarioFinal.objects.get(pk=id_usuario)
				mensaje = { "status": "True", "usuario_id": usuario.id }
				usuario.delete()
				usuario.user.delete()
				return HttpResponse(json.dumps(mensaje))
			except:
				mensaje = { "status": "False" }
				return HttpResponse(json.dumps(mensaje))

	def get_context_data(self, **kwargs):
		context = super(UsuarioFinalListView, self).get_context_data(**kwargs)
		context['q'] = self.request.GET.get('q', '')
		return context

@permission_required('auth.add_user', login_url='/login/')
@login_required(login_url='/login/')
def RegisterUsuarioFinalView(request): # Vista encargada de mostrar el formulario de registro
	if request.method == 'POST': # Verifica si la peticion hecha por el usuario es POST
		if 'submit-agregar' in request.POST:
			form_csv = UsuarioCSVForm()
			form = RegistrationUsuarioFinalForm(data=request.POST) # Creamos una instancia y le pasamos los datos del formulario
			if form.is_valid(): # Verificar si los campos fueron validados correctamente
				user = form.save() # Guarda un usuario con los datos dados en el formulario
				usuario = form.cleaned_data['username'] # Guardamos el nombre del usuario con ayuda de la variable cleaned_data
				messages.info(request, 'Usuario %s agregado correctamente' % usuario) # Creamos un mensaje de exito para mostrarlo en la otra vista
				return redirect('/lista-usuarios/') # Nos redirijimos a la vista lista_usuarios
		elif 'submit-csv' in request.POST:
			form = RegistrationUsuarioFinalForm()
			form_csv = UsuarioCSVForm(request.POST, request.FILES)
			if form_csv.is_valid():
				importarCSV(request.FILES['archivoCSV'])
				return redirect('/lista-usuarios/') # Nos redirijimos a la vista lista_usuarios
	else:
		form = RegistrationUsuarioFinalForm() # En caso de no ser una peticion POST se crea la instancia del formulario
		form_csv = UsuarioCSVForm()
	return render_to_response('usuarios_agregar.html', { 'form': form, 'form_csv': form_csv }, context_instance=RequestContext(request)) # Renderizamos el formulario para que se muestra en el template

class UsuarioFinalUpdateView(UpdateView): # Vista que hereda de UpdateView para actualizar un objeto ya creado
	#form_class = UsuarioFinalChangeForm # Especificamos el formulario a usar
	template_name = 'modificar_usuario.html' # Especificamos la plantilla a renderizar
	model = User # Especificamos el modelo en donde buscara el objeto a actualizar
	fields = ['first_name', 'last_name', 'email']

	def form_valid(self, form): # Sobreescribimos el metodo form_valid para cambiar su comportamiento
		self.object = form.save() # Actualizamos el objeto con sus cambios y retorna ese mismo objeto
		request = self.request # Asignamos a una variable local el self.request
		messages.info(request, 'Usuario actualizado') # Mandamos un mensaje de informacion especificando que se ha modificado el cupon
		return super(BaseUpdateView, self).get(request) # Mandamos a llamar al padre de get para que renderize de vuelta el formulario

def PromotorView(request):
	promotores = Promotor.objects.all()
	if request.method == 'POST':
		form = RegistrationUsuarioPromotorForm(request.POST)
		if form.is_valid():
			promotor = form.save()
			messages.info(request, 'Usuario promotor %s agregado' % promotor)
			form = RegistrationUsuarioPromotorForm()
			return render(request, 'promotores.html', { 'promotores': promotores, 'form': form })
	else:
		form = RegistrationUsuarioPromotorForm()
	return render(request, 'promotores.html', { 'promotores': promotores, 'form': form })

@permission_required('userprofiles.change_afiliado', login_url='/login/')
@login_required(login_url='/login/')
def AdministrarPerfilAfiliadoView(request, usuario):
	user_afiliado = get_object_or_404(User, username=request.user.username)
	afiliado = get_object_or_404(Afiliado, id=request.user.perfil_afiliado.id)
	if request.method == 'POST':
		user_username = user_afiliado.username
		form_user = UserAfiliadoUpdateForm(request.POST, instance=user_afiliado)
		form_afiliado = PerfilAfiliadoUpdateForm(request.POST, request.FILES, instance=afiliado)
		if form_user.is_valid() and form_afiliado.is_valid():
			user = form_user.save()
			form_afiliado.save()
			if user_username == user.username:
				messages.info(request, 'Perfil actualizado') # Creamos un mensaje de exito para mostrarlo en la otra vista
				if afiliado.facebook != '':
					datos = afiliado.facebook.split('.com/')
					afiliado.facebook = datos[1]
				if afiliado.twitter != '':
					datos = afiliado.twitter.split('.com/')
					afiliado.twitter = datos[1]
				form_user = UserAfiliadoUpdateForm(instance=user_afiliado)
				form_afiliado = PerfilAfiliadoUpdateForm(instance=afiliado)
			else:
				messages.info(request, 'Perfil actualizado. Vuelva a iniciar sesión con su nuevo username') # Creamos un mensaje de exito para mostrarlo en la otra vista
				return redirect('/logout/')
	else:
		if afiliado.facebook != '':
			datos = afiliado.facebook.split('.com/')
			afiliado.facebook = datos[1]
		if afiliado.twitter != '':
			datos = afiliado.twitter.split('.com/')
			afiliado.twitter = datos[1]
		form_user = UserAfiliadoUpdateForm(instance=user_afiliado)
		form_afiliado = PerfilAfiliadoUpdateForm(instance=afiliado)
	return render(request, 'modificar_perfil.html', { 'form_user': form_user, 'form_afiliado': form_afiliado })

@permission_required('userprofiles.delete_local', login_url='/login/')
@login_required(login_url='/login/')
def AfiliadoLocalDeleteView(request, usuario):
	afiliado = get_object_or_404(Afiliado, user__username=request.user.username)
	locales = afiliado.locales.all()
	if request.method == 'POST':
		if 'local_id' in request.POST:
			try:
				id_local = request.POST['local_id']
				local = Local.objects.get(pk=id_local)
				mensaje = { "status": "True", "local_id": local.id }
				local.delete()
				return HttpResponse(json.dumps(mensaje))
			except:
				mensaje = { "status": "False" }
				return HttpResponse(json.dumps(mensaje))
	return render_to_response('afiliado_locales.html', { 'locales': locales }, context_instance=RequestContext(request))

@permission_required('userprofiles.add_local', login_url='/login/')
@login_required(login_url='/login/')
def AfiliadoLocalUpdateView(request, usuario):
	afiliado = get_object_or_404(Afiliado, user__username=request.user.username)
	if request.method == 'POST':
		json_locales = request.read()
		locales = json.loads(json_locales)
		if afiliado.user.username == usuario:
			i = 0
			num_locales = len(locales['direcciones'])
			while i < num_locales:
				local_afiliado = Local(direccion=locales['direcciones'][i], latitud=locales['latitudes'][i], longitud=locales['longitudes'][i], local_afiliado=afiliado)
				local_afiliado.save()
				i += 1
			messages.info(request, 'Locales agregados correctamente') # Creamos un mensaje de exito para mostrarlo en la otra vista
			return HttpResponse('/%s/locales' % request.user.username)
	return render_to_response('afiliado_modificar_locales.html', context_instance=RequestContext(request))

@permission_required('userprofiles.change_afiliado', login_url='/login/')
@login_required(login_url='/login/')
def AfiliadoPasswordChangeView(request, usuario):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.info(request, 'Contraseña actualizada. Introduzca su nueva contraseña.') # Creamos un mensaje de exito para mostrarlo en la otra vista
			return redirect('/login/')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'modificar_password.html', { 'form': form })

from django.core.mail.message import EmailMultiAlternatives
from django.http.response import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
 
 
def enviar_correo(request):
	if request.method == 'POST':
		form = PasswordResetForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse("Correo enviado")
	else:
		form = PasswordResetForm()
	return render(request, 'email.html', { 'form': form })

# Django REST Framework -----------------------------------------------------------------------------------------------------------------

from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .serializers import AfiliadoSerializer, AfiliadoCuponesSerializer, AfiliadoPromocionesSerializer, AfiliadoCartelSerializer, LocalSerializer, UserSerializer

class AfiliadoAPIView(generics.ListAPIView):
	queryset = Afiliado.objects.filter(user__is_active=True)
	serializer_class = AfiliadoSerializer

class AfiliadoDetailAPIView(generics.RetrieveAPIView):
	queryset = Afiliado.objects.all()
	serializer_class = AfiliadoSerializer

class AfiliadoCuponesAPIView(generics.ListAPIView):
	queryset = Afiliado.objects.filter(user__is_active=True)
	serializer_class = AfiliadoCuponesSerializer

class AfiliadoPromocionesAPIView(generics.ListAPIView):
	queryset = Afiliado.objects.filter(user__is_active=True)
	serializer_class = AfiliadoPromocionesSerializer

class AfiliadoCartelAPIView(generics.ListAPIView):
	queryset = Afiliado.objects.all().order_by('?')[:10]
	serializer_class = AfiliadoCartelSerializer

class UsuariosCuponesAfiliados(APIView):
	def get(self, request, usuario, format=None):
		afiliados = Afiliado.objects.exclude(cupones__users__username=usuario).filter(cupones__status='Activo', user__is_active=True)
		serializer = AfiliadoCuponesSerializer(afiliados, many=True)
		return Response(serializer.data)

class LocalAfiliadoAPIView(generics.ListAPIView):
	serializer_class = LocalSerializer
	"""
		Sobreescribimos el metodo get_queryset, para que nos devuelva
		una consulta, que seran los cupones de cada afiliado.
	"""
	def get_queryset(self):
		local_afiliado = self.kwargs['local_afiliado'] # Desde la URL por medio de los kwargs le pasamos el id del afiliado
		return Local.objects.filter(local_afiliado=local_afiliado) # Retorna un tipo de dato queryset para mostrarse en la vista

@api_view(['POST'])
def iniciar_sesion(request):
	if request.method == 'POST':
		#data = JSONParser().parse(request)
		data = request.data
		usuario = data['usuario']
		clave = data['clave']
		respuesta = {}
		try:
			usuario_final = UsuarioFinal.objects.get(user__username=usuario)
		except UsuarioFinal.DoesNotExist:
			respuesta['estado'] = "False"
			return Response(respuesta)
		else:
			if usuario_final.user.check_password(clave):
				respuesta['estado'] = "True"
				return Response(respuesta)
			else:
				respuesta['estado'] = "False"
				return Response(respuesta)

@api_view(['POST'])
def cambiar_clave(request):
	if request.method == 'POST':
		#data = JSONParser().parse(request)
		data = request.data
		usuario = data['usuario']
		clave = data['clave']
		respuesta = {}
		try:
			usuario_final = UsuarioFinal.objects.get(user__username=usuario)
		except UsuarioFinal.DoesNotExist:
			respuesta['estado'] = "False"
			return Response(respuesta)
		else:
			usuario_final.user.set_password(clave)
			usuario_final.user.save()
			respuesta['estado'] = "True"
			return Response(respuesta)

class CorreoUsuarioFinalAPIView(APIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_object(self, username):
		try:
			return User.objects.get(username=username)
		except User.DoesNotExist:
			raise Http404

	def get(self, request, username, format=None):
		usuario = self.get_object(username)
		serializer = UserSerializer(usuario)
		return Response(serializer.data)

"""class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer"""
