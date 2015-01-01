# -*- encoding: utf-8 -*-
import json
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic import ListView, FormView
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout
from .decorators import is_promotor
from .forms import LoginForm, UserAfiliadoForm, PerfilAfiliadoForm, UsuarioCSVForm, LocalForm, RegistrationUsuarioPromotorForm, RegistrationUsuarioFinalForm
from .mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Afiliado, Local
from .load_data import importarCSV

class LoginUserPromotorView(FormView):
	#model = UsuarioPromotor
	template_name = 'login.html'
	success_url = '/agregar-usuarios/'
	form_class = LoginForm

	def form_valid(self, form):
		login(self.request, form.user_cache)
		return super(LoginUserPromotorView, self).form_valid(form)

class UsuarioPromotorListView(ListView):
	model = User
	template_name = 'lista_usuarios.html'

class UsuarioFinalListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission = 'auth.change_user'
	queryset = User.objects.filter(groups__name='Usuario')
	template_name = 'lista_usuarios.html'

class AfiliadoListView(LoginRequiredMixin, ListView):
	queryset = Afiliado.objects.all()
	template_name = 'lista_empresas.html'

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
			return HttpResponse('/lista-usuarios/')
	return render_to_response('locales.html', {}, context_instance=RequestContext(request))

@permission_required('userprofiles.add_afiliado', login_url='/login/')
@login_required(login_url='/login/')
def AfiliadoView(request):
	if request.method == 'POST': # Verifica si la peticion hecha por el usuario es POST
		form_user = UserAfiliadoForm(request.POST) # Se crea una instancia del formulario UserAfiliadoForm y le pasamos los datos del formulario
		form_afiliado = PerfilAfiliadoForm(request.POST, request.FILES) # Se crea una instancia del formulario PerfilAfiliadoForm y le pasamos los datos junto con los archivo subidos
		if form_user.is_valid() and form_afiliado.is_valid(): # Verificamos si los formularios pasaron todas sus validaciones
			usuario = form_user.save() # Se crea el usuario
			afiliado = form_afiliado.guardarAfiliado(usuario) # Se manda a llamar a un metodo declarado en el formulario para que guarda al afiliado
			if 'submit-guardar-salir' in request.POST:
				return redirect('/lista-afiliados/')
			elif 'submit-guardar-locales' in request.POST:
				return redirect('/agregar-locales/' + form_user.cleaned_data['username'] + '/' + usuario.id + '/')
	else:
		form_user = UserAfiliadoForm()
		form_afiliado = PerfilAfiliadoForm()
	return render_to_response('afiliados_agregar.html', { 'form_user': form_user, 'form_afiliado': form_afiliado }, context_instance=RequestContext(request))

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

def lista_usuarios_view(request):
	return render(request, 'lista_usuarios.html')

def logout_view(request):
	logout(request)
	return redirect('/login/')