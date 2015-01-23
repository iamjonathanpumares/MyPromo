# -*- encoding: utf-8 -*-
import json
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.views.generic import ListView, FormView, UpdateView
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout
from .forms import LoginForm, UserAfiliadoForm, PerfilAfiliadoForm, UsuarioCSVForm, LocalForm, RegistrationUsuarioPromotorForm, RegistrationUsuarioFinalForm, StatusUpdateForm
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

"""def entrar(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			login(request, form.user_cache)
			if request.user"""


# Logout -----------------------------------------------------------------------------------------------------
def logout_view(request):
	logout(request)
	return redirect('/login/')

# Home -------------------------------------------------------------------------------------------------------
@login_required(login_url='/login/')
def home(request):
	num_afiliados = Afiliado.objects.all().count()
	num_usuarios = UsuarioFinal.objects.all().count()
	if request.user.is_superuser == True:
		return render(request, 'home.html', { 'num_afiliados': num_afiliados, 'num_usuarios': num_usuarios })
	try:
		request.user.groups.get(name='Promotor')
	except Group.DoesNotExist:
		try:
			request.user.groups.get(name='Afiliado')
		except Group.DoesNotExist:
			raise Http404
		else:
			return redirect('/%s/' % request.user.username)
	else:
		return render(request, 'home.html', { 'num_afiliados': num_afiliados, 'num_usuarios': num_usuarios })

def home_afiliado(request, usuario):
	afiliado = get_object_or_404(Afiliado, user__username=usuario)
	return render(request, 'home_afiliado.html')



# Views Afiliado ---------------------------------------------------------------------------------------------
class AfiliadoListView(LoginRequiredMixin, ListView):
	queryset = Afiliado.objects.all()
	template_name = 'lista_empresas.html'

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
	model = UsuarioFinal
	#queryset = User.objects.filter(groups__name='Usuario')
	template_name = 'lista_usuarios.html'

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
def AdministrarAfiliadoView(request):
	if request.method == 'POST': # Verifica si la peticion hecha por el usuario es POST
		form_afiliado = PerfilAfiliadoForm(request.POST, request.FILES) # Se crea una instancia del formulario PerfilAfiliadoForm y le pasamos los datos junto con los archivo subidos
		if form_user.is_valid() and form_afiliado.is_valid(): # Verificamos si los formularios pasaron todas sus validaciones
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

# Django REST Framework -----------------------------------------------------------------------------------------------------------------

from rest_framework import viewsets, generics
from .serializers import AfiliadoSerializer, AfiliadoCuponesSerializer, AfiliadoPromocionesSerializer, LocalSerializer

class AfiliadoAPIView(generics.ListAPIView):
	queryset = Afiliado.objects.filter(user__is_active=True)
	serializer_class = AfiliadoSerializer

class AfiliadoCuponesAPIView(generics.ListAPIView):
	queryset = Afiliado.objects.filter(user__is_active=True)
	serializer_class = AfiliadoCuponesSerializer

class AfiliadoPromocionesAPIView(generics.ListAPIView):
	queryset = Afiliado.objects.filter(user__is_active=True)
	serializer_class = AfiliadoPromocionesSerializer

class LocalAfiliadoAPIView(generics.ListAPIView):
	serializer_class = LocalSerializer

	"""
		Sobreescribimos el metodo get_queryset, para que nos devuelva
		una consulta, que seran los cupones de cada afiliado.
	"""
	def get_queryset(self):
		local_afiliado = self.kwargs['local_afiliado'] # Desde la URL por medio de los kwargs le pasamos el id del afiliado
		return Local.objects.filter(local_afiliado=local_afiliado) # Retorna un tipo de dato queryset para mostrarse en la vista

"""class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer"""
