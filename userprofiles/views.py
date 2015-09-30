# -*- encoding: utf-8 -*-
import json
from cupones.models import Cupon
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import Group, User
from django.db.models import Count, Q
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView, FormView, UpdateView, TemplateView, DetailView
from django.views.generic.edit import BaseUpdateView
from promociones.models import Promocion
from .decorators import redirect_home
from .forms import LoginForm, UserAfiliadoForm, UserAfiliadoUpdateForm, PerfilAfiliadoForm, PerfilAfiliadoUpdateForm, UsuarioCSVForm, RegistrationUsuarioPromotorForm, RegistrationUsuarioFinalForm, StatusUpdateForm, UsuarioFinalForm, UserUpdateForm, PromotorUpdateForm
from .mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Afiliado, UsuarioFinal, Promotor, Giro
from .tasks import importarCSV, convertirCSV

# Imports para enviar correo
from django.core.mail.message import EmailMultiAlternatives
from django.http.response import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Signup ----------------------------------------------------------------------------------------------------
def SignupView(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			usuario = form.save()
			return redirect('/login/')
	else:
		form = SignupForm()
	return render(request, 'userprofiles/signup.html', { 'form': form })

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

# Inicio del Promotor -------------------------------------------------------------------------------------------------------
@redirect_home
def home(request):
	promocion_popular = Promocion.objects.annotate(Count('users')).order_by('users__count').reverse()[:1]
	cupon_popular = Cupon.objects.annotate(Count('users')).order_by('-users__count', '-usuarioscupones__fecha')[:1]
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

# Familia UNID - Agregar -----------------------------------------------------------------------------------------------
@permission_required('auth.add_user', login_url='/login/')
@login_required(login_url='/login/')
def RegisterUsuarioFinalView(request): # Vista encargada de mostrar el formulario de registro
	if request.method == 'POST': # Verifica si la peticion hecha por el usuario es POST
		if 'submit-agregar' in request.POST:
			form_csv = UsuarioCSVForm()
			form_user = RegistrationUsuarioFinalForm(data=request.POST) # Creamos una instancia y le pasamos los datos del formulario
			form = UsuarioFinalForm(request.POST)
			if form_user.is_valid() and form.is_valid(): # Verificar si los campos fueron validados correctamente
				user = form_user.save() # Guarda un usuario con los datos dados en el formulario
				usuario_final = form.save(commit=False)
				usuario_final.user = user
				usuario_final.save()
				messages.info(request, 'Usuario %s agregado correctamente' % form_user.cleaned_data['username']) # Creamos un mensaje de exito para mostrarlo en la otra vista
				return redirect('/lista-usuarios/') # Nos redirijimos a la vista lista_usuarios
		elif 'submit-csv' in request.POST:
			checked = True if 'checkcsv' in request.POST else False # Preguntamos si en el formulario le dieron checked a nuestro checkbox. True si fue checked, False si no le dieron checked
			form_user = RegistrationUsuarioFinalForm()
			form = UsuarioFinalForm()
			form_csv = UsuarioCSVForm(request.POST, request.FILES)
			if form_csv.is_valid():
				lista_usuarios = convertirCSV(request.FILES['archivoCSV'])
				if importarCSV.delay(lista_usuarios, request.user.username, checked):
					messages.info(request, 'Su base de datos se cargara en breve. Le avisaremos cuando este lista. Puede seguir trabajando.')	
					return redirect('/home/') # Nos redirijimos a la vista lista_usuarios
	else:
		form_user = RegistrationUsuarioFinalForm() # En caso de no ser una peticion POST se crea la instancia del formulario
		form = UsuarioFinalForm()
		form_csv = UsuarioCSVForm()
	return render_to_response('usuarios_agregar.html', { 'form_user': form_user, 'form': form, 'form_csv': form_csv }, context_instance=RequestContext(request)) # Renderizamos el formulario para que se muestra en el template

# Familia UNID - Modificar(Lista de usuarios) ----------------------------------------------------------------------------------------------
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
		    object_list = UsuarioFinal.objects.filter(full_name__icontains=name)
		    self.paginate_by = None
		else:
		    object_list = UsuarioFinal.objects.all().order_by('full_name')
		    self.paginate_by = 15
		return object_list

	def post(self, request, *args, **kwargs):
		# Elimina un usuario en la lista
		if 'usuario_id' in request.POST:
			try:
				id_usuario = request.POST['usuario_id']
				usuario = UsuarioFinal.objects.get(pk=id_usuario)
				mensaje = { "status": "True", "usuario_id": usuario.id, "action": "Eliminar" }
				usuario.delete()
				usuario.user.delete()
				return HttpResponse(json.dumps(mensaje))
			except:
				mensaje = { "status": "False", "action": "Eliminar" }
				return HttpResponse(json.dumps(mensaje))

		# Envia un correo a un usuario en la lista		
		if 'id_usuario' in request.POST:
			try:
				id_usuario = request.POST['id_usuario']
				usuario = UsuarioFinal.objects.get(pk=id_usuario)
				email_context = {
					'titulo': 'Bienvenido a MyPromo UNID, la nueva experiencia de ver tus promociones.',
					'matricula': usuario.user.username,
					'nombre': usuario.full_name
				}
				# Se renderiza el template con el context
				email_html = render_to_string('email.html', email_context)

				# Se quitan las etiquetas html para que quede en texto plano
				email_text = strip_tags(email_html)

				correo = EmailMultiAlternatives(
					'Bienvenido a MyPromo UNID',
					email_text,
					'veltiumdevelopment@gmail.com',
					[usuario.user.email],
				)

				# Se especifica que el contenido es html
				correo.attach_alternative(email_html, 'text/html')

				# Se envia el correo
				correo.send()
				mensaje = { "status": "True", "action": "Enviar" }
				return HttpResponse(json.dumps(mensaje))
			except:
				mensaje = { "status": "False", "action": "Enviar" }
				return HttpResponse(json.dumps(mensaje))

	def get_context_data(self, **kwargs):
		context = super(UsuarioFinalListView, self).get_context_data(**kwargs)
		context['q'] = self.request.GET.get('q', '')
		return context

# Familia UNID - Modificar(Actualizar usuario) ------------------------------------------------------------------
def UsuarioFinalUpdateView(request, pk): # Vista que hereda de UpdateView para actualizar un objeto ya creado
	usuario_user = get_object_or_404(User, id=pk)
	usuario_final = get_object_or_404(UsuarioFinal, user__id=pk)
	if request.method == 'POST':
		form_user = UserUpdateForm(request.POST, instance=usuario_user)
		form = UsuarioFinalForm(request.POST, instance=usuario_final)
		if form_user.is_valid() and form.is_valid():
			form_user.save()
			form.save()
			messages.info(request, 'Usuario actualizado')
			return render(request, 'modificar_usuario.html', { 'form_user': form_user, 'form': form })
	else:
		form_user = UserUpdateForm(instance=usuario_user)
		form = UsuarioFinalForm(instance=usuario_final)
	return render(request, 'modificar_usuario.html', { 'form_user': form_user, 'form': form })

# Afiliados - Agregar -------------------------------------------------------------------------------------------
@permission_required('userprofiles.add_afiliado', login_url='/login/')
@login_required(login_url='/login/')
def AfiliadoView(request):
	giros = Giro.objects.all()
	valida_giro = ''
	if request.method == 'POST': # Verifica si la peticion hecha por el usuario es POST
		if 'submit-agregar-giro' in request.POST:
			giro = request.POST['txt-giro']
			if giro.strip() == '':
				mensaje = { "status": "False", "msj": "Escriba un giro"}
				return HttpResponse(json.dumps(mensaje))
				#return redirect('/lista-afiliados/')
			else:
				giro = Giro.objects.create(giro=giro)
				mensaje = { "status": "True", "msj": "Giro agregado con éxito", "nombre_giro": giro.giro }
				return HttpResponse(json.dumps(mensaje))
		elif 'submit-guardar-salir' in request.POST or 'submit-guardar-locales' in request.POST:
			
			form_user = UserAfiliadoForm(request.POST) # Se crea una instancia del formulario UserAfiliadoForm y le pasamos los datos del formulario
			form_afiliado = PerfilAfiliadoForm(request.POST, request.FILES) # Se crea una instancia del formulario PerfilAfiliadoForm y le pasamos los datos junto con los archivo subidos
			if form_user.is_valid() and form_afiliado.is_valid(): # Verificamos si los formularios pasaron todas sus validaciones
				if request.POST['select-giro'] != '':
					usuario = form_user.save() # Se crea el usuario
					afiliado = form_afiliado.save(commit=False) # Se manda a llamar a un metodo declarado en el formulario para que guarda al afiliado
					afiliado.codigoValidacion = User.objects.make_random_password(length=100)
					afiliado.giro = request.POST['select-giro']
					afiliado.user = usuario
					afiliado.save()

					if 'submit-guardar-salir' in request.POST:
						messages.info(request, 'Afiliado %s agregado' % form_afiliado.cleaned_data['nombreEmpresa'])
						return redirect('/lista-afiliados/')
					elif 'submit-guardar-locales' in request.POST:
						return redirect('/agregar-locales/' + form_user.cleaned_data['username'] + '/' + str(usuario.id) + '/')

				else:
					valida_giro = 'Escoja un giro o agregue uno'

				
			
	else:
		form_user = UserAfiliadoForm()
		form_afiliado = PerfilAfiliadoForm()
	return render_to_response('afiliados_agregar.html', { 'form_user': form_user, 'form_afiliado': form_afiliado, 'giros': giros, 'valida_giro': valida_giro }, context_instance=RequestContext(request))

# Afiliados - Agregar - Guardar y agregar locales -------------------------------------------------------------------
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

# Afiliados - Modificar ---------------------------------------------------------------------------------------------
class AfiliadoListView(LoginRequiredMixin, ListView):
	model = Afiliado
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

# Afiliados - Modificar - Status ------------------------------------------------------------------------------------
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

# Afiliados - Modificar - Update -------------------------------------------------------------------------------------
def AfiliadoUpdateView(request, usuario, id): # Vista que hereda de UpdateView para actualizar un objeto ya creado
	user_afiliado = get_object_or_404(User, username=usuario)
	afiliado = get_object_or_404(Afiliado, id=id)
	giros = Giro.objects.all()
	valida_giro = ''
	if request.method == 'POST':
		if 'submit-agregar-giro' in request.POST:
			giro = request.POST['txt-giro']
			if giro.strip() == '':
				mensaje = { "status": "False", "msj": "Escriba un giro"}
				return HttpResponse(json.dumps(mensaje))
				#return redirect('/lista-afiliados/')
			else:
				giro = Giro.objects.create(giro=giro)
				mensaje = { "status": "True", "msj": "Giro agregado con éxito", "nombre_giro": giro.giro }
				return HttpResponse(json.dumps(mensaje))

		elif 'submit-guardar-salir' in request.POST:
			form_user = UserAfiliadoUpdateForm(request.POST, instance=user_afiliado)
			form_afiliado = PerfilAfiliadoUpdateForm(request.POST, request.FILES, instance=afiliado)
			if form_user.is_valid() and form_afiliado.is_valid():
				if request.POST['select-giro'] != '':
					form_user.save()
					afiliado_instance_form = form_afiliado.save()
					afiliado_instance_form.giro = request.POST['select-giro']
					afiliado_instance_form.save()
					messages.info(request, 'Afiliado %s modificado' % afiliado) # Creamos un mensaje de exito para mostrarlo en la otra vista
					return redirect('/lista-afiliados/')
				else:
					valida_giro = 'Escoja un giro o agregue uno'

	else:
		if afiliado.facebook != '':
			datos = afiliado.facebook.split('.com/')
			afiliado.facebook = datos[1]
		if afiliado.twitter != '':
			datos = afiliado.twitter.split('.com/')
			afiliado.twitter = datos[1]
		form_user = UserAfiliadoUpdateForm(instance=user_afiliado)
		form_afiliado = PerfilAfiliadoUpdateForm(instance=afiliado)
	return render(request, 'modificar_afiliado.html', { 'form_user': form_user, 'form_afiliado': form_afiliado, 'afiliado': afiliado, 'giros': giros, 'valida_giro': valida_giro })

# Afiliados - Modificar - Locales --------------------------------------------------------------------------------------
@permission_required('userprofiles.delete_local', login_url='/login/')
@login_required(login_url='/login/')
def LocalListDeleteView(request, usuario, id):
	afiliado = get_object_or_404(Afiliado, user__username=usuario, id=id)
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
	return render_to_response('lista_locales.html', { 'afiliado': afiliado, 'locales': locales }, context_instance=RequestContext(request))

@permission_required('userprofiles.add_local', login_url='/login/')
@login_required(login_url='/login/')
def LocalUpdateView(request, usuario, id):
	afiliado = get_object_or_404(Afiliado, user__username=usuario, id=id)
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
			return HttpResponse('/lista-locales/%s/%s/' % (afiliado.user.username, afiliado.id))
	return render_to_response('modificar_locales.html', context_instance=RequestContext(request))

# Administrar - Usuarios promotor (Lista de usuarios) ----------------------------------------------------------------------------------
def PromotorView(request):
	promotores = Promotor.objects.all()
	if request.method == 'POST':
		# Elimina un usuario en la lista
		if 'usuario_id' in request.POST:
			try:
				id_usuario = request.POST['usuario_id']
				promotor = Promotor.objects.get(pk=id_usuario)
				mensaje = { "status": "True", "usuario_id": promotor.id, "action": "Eliminar" }
				promotor.delete()
				promotor.user.delete()
				return HttpResponse(json.dumps(mensaje))
			except:
				mensaje = { "status": "False", "action": "Eliminar" }
				return HttpResponse(json.dumps(mensaje))
	return render(request, 'promotores.html', { 'promotores': promotores })

# Administrar - Usuarios promotor (Agregar) ----------------------------------------------------------------------------------
def PromotorCreateView(request):
	if request.method == 'POST':
		form = RegistrationUsuarioPromotorForm(request.POST)
		if form.is_valid():
			promotor = form.save()
			messages.info(request, 'Usuario promotor %s agregado' % promotor)
			return redirect('/administrar-usuarios/')
	else:
		form = RegistrationUsuarioPromotorForm()
	return render(request, 'promotor_form.html', { 'form': form })

# Administrar - Usuarios promotor (Actualizar) ----------------------------------------------------------------------------------
def PromotorUpdateView(request, pk):
	user_promotor = get_object_or_404(User, id=pk)
	if request.method == 'POST':
		form = PromotorUpdateForm(request.POST, instance=user_promotor)
		if form.is_valid():
			promotor = form.save()
			messages.info(request, 'Usuario promotor %s modificado' % promotor)
			return render(request, 'promotor_update.html', { 'form': form })
	else:
		form = PromotorUpdateForm(instance=user_promotor)
	return render(request, 'promotor_update.html', { 'form': form })

# ScanCard --------------------------------------------------------------------------------------------------------
class ScanCardListView(LoginRequiredMixin, ListView): # Vista que hereda de ListView para mostrar la lista de afiliados
	model = Afiliado # Especificamos el modelo para traernos todos los objetos y mostrar la lista
	template_name = 'scancards_afiliados.html' # Template que sera renderizado para mostrar la lista de afiliados

# ScanCard - Ver ScanCard -----------------------------------------------------------------------------------------
class ScanCardView(DetailView):
	model = Afiliado
	template_name = 'afiliado_scancard.html'

class UsuarioPromotorListView(ListView):
	model = User
	template_name = 'lista_usuarios.html'

@permission_required('userprofiles.change_afiliado', login_url='/login/')
@login_required(login_url='/login/')
def AdministrarPerfilAfiliadoView(request, usuario):
	user_afiliado = get_object_or_404(User, username=request.user.username)
	afiliado = get_object_or_404(Afiliado, id=request.user.perfil_afiliado.id)
	giros = Giro.objects.all()
	valida_giro = ''
	if request.method == 'POST':
		if 'submit-agregar-giro' in request.POST:
			giro = request.POST['txt-giro']
			if giro.strip() == '':
				mensaje = { "status": "False", "msj": "Escriba un giro"}
				return HttpResponse(json.dumps(mensaje))
				#return redirect('/lista-afiliados/')
			else:
				giro = Giro.objects.create(giro=giro)
				mensaje = { "status": "True", "msj": "Giro agregado con éxito", "nombre_giro": giro.giro }
				return HttpResponse(json.dumps(mensaje))

		elif 'submit-actualizar' in request.POST:
			user_username = user_afiliado.username
			form_user = UserAfiliadoUpdateForm(request.POST, instance=user_afiliado)
			form_afiliado = PerfilAfiliadoUpdateForm(request.POST, request.FILES, instance=afiliado)
			if form_user.is_valid() and form_afiliado.is_valid():
				if request.POST['select-giro'] != '':
					user = form_user.save()
					afiliado_instance_form = form_afiliado.save()
					afiliado_instance_form.giro = request.POST['select-giro']
					afiliado_instance_form.save()
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
					valida_giro = 'Escoja un giro o agregue uno'
	else:
		if afiliado.facebook != '':
			datos = afiliado.facebook.split('.com/')
			afiliado.facebook = datos[1]
		if afiliado.twitter != '':
			datos = afiliado.twitter.split('.com/')
			afiliado.twitter = datos[1]
		form_user = UserAfiliadoUpdateForm(instance=user_afiliado)
		form_afiliado = PerfilAfiliadoUpdateForm(instance=afiliado)
	return render(request, 'modificar_perfil.html', { 'form_user': form_user, 'form_afiliado': form_afiliado, 'giros': giros })

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

@login_required(login_url='/login/')
def AfiliadoEstadisticasView(request, usuario):
	cupones = Cupon.objects.filter(cupon_afiliado__user__username=usuario).annotate(Count('users')).order_by('users__count').reverse()
	promociones = Promocion.objects.filter(promocion_afiliado__user__username=usuario).annotate(Count('users')).order_by('users__count').reverse()
	return render(request, 'afiliado_estadisticas.html', { 'cupones': cupones, 'promociones': promociones })

def enviar_correo(request):
    email_context = {
        'titulo': 'Titulo correo',
        'usuario': 'Jonathan Pumares',
        'mensaje': 'mensaje del correo',
    }
    # se renderiza el template con el context
    email_html = render_to_string('email.html', email_context)
 
    # se quitan las etiquetas html para que quede en texto plano
    email_text = strip_tags(email_html)
 
    correo = EmailMultiAlternatives(
        'Asunto del correo',  # Asunto
        email_text,  # contenido del correo
        'origen@ejemplo.com',  # quien lo envía
        ['jepc1491@gmail.com'],  # a quien se envía
    )
 
    # se especifica que el contenido es html
    correo.attach_alternative(email_html, 'text/html')
    # se envía el correo
    correo.send()
    return HttpResponseRedirect('/')

# Django REST Framework -----------------------------------------------------------------------------------------------------------------

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from cupones.serializers import CuponSerializer
from .serializers import *

@api_view(['POST'])
@permission_classes((AllowAny,))
def SignupAPIView(request):
	if request.method == 'POST':
		serializer = SignupSerializer(data=request.data)
		if serializer.is_valid():
			username = serializer.data['username']
			password = serializer.data['password']
			email = serializer.data['email']

			UserModel = get_user_model()
			user = UserModel()
			user.username = username
			user.set_password(password)
			user.email = email
			user.is_active = True
			user.save()

			token = Token.objects.create(user=user)
			return Response({ 'token': token.key })
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AfiliadoAPIView(generics.ListAPIView):
	queryset = Afiliado.objects.filter(user__is_active=True)
	serializer_class = AfiliadoSerializer

class AfiliadoDetailAPIView(generics.RetrieveAPIView):
	queryset = Afiliado.objects.all()
	serializer_class = AfiliadoSerializer

class AfiliadoCuponesAPIView(generics.ListAPIView):
	queryset = Afiliado.objects.filter(user__is_active=True)
	serializer_class = AfiliadoCuponesSerializer

# TODO: Validar solo las promociones que estan activas
class AfiliadoPromocionesAPIView(generics.ListAPIView):
	queryset = Afiliado.objects.filter(user__is_active=True)
	serializer_class = AfiliadoPromocionesSerializer

@api_view(['GET'])
def AfiliadoCuponesPromocionesAPIView(request, usuario):
	afiliados_queryset = Afiliado.objects.filter(user__is_active=True)
	serializer = AfiliadoCuponesPromocionesSerializer(afiliados_queryset, many=True, context={ 'request': request, 'usuario': usuario })
	#serializer.get_cupones_active(afiliados_queryset, usuario)

	#cupones_queryset = Cupon.objects.filter(status='Activo')
	#cupones_serializer = CuponSerializer(cupones_queryset, many=True)
	#serializer.cupones = cupones_serializer
	return Response(serializer.data)

def api_root(request, format=None):
	return Response({
		''
	})

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

@api_view(['GET'])
def RatingUsuarioFinalAPIView(request, usuario):
	usuario_final_queryset = UsuarioFinal.objects.filter(user__username=usuario)
	serializer = UsuarioFinalSerializer(usuario_final_queryset, many=True)
	#serializer.get_cupones_active(afiliados_queryset, usuario)

	#cupones_queryset = Cupon.objects.filter(status='Activo')
	#cupones_serializer = CuponSerializer(cupones_queryset, many=True)
	#serializer.cupones = cupones_serializer
	return Response(serializer.data)

@api_view(['POST'])
def RatingCreateAPIView(request):
	if request.method == 'POST':
		# Capturo los datos mandados por JSON
		username = request.data['username']
		id_afiliado = request.data['id_afiliado']
		puntuacion = request.data['puntuacion']

		# Intento buscar al usuario final y al afiliado objects
		try:
			usuario_final = UsuarioFinal.objects.get(user__username=username)
			afiliado = Afiliado.objects.get(pk=id_afiliado)
		except (UsuarioFinal.DoesNotExist, Afiliado.DoesNotExist):
			return Response(status=status.HTTP_404_NOT_FOUND)

		# Se crea un nuevo rating y se retorna un mensaje de creado
		rating = Rating.objects.create(usuario_final=usuario_final, afiliado=afiliado, puntuacion=puntuacion)
		return Response({ 'mensaje': 'Rating creado' }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def RatingUpdateAPIView(request):
	if request.method == 'POST':
		# Capturo los datos mandados por JSON
		id_rating = request.data['id_rating']
		puntuacion = request.data['puntuacion']

		# Intento buscar al rating object
		try:
			rating = Rating.objects.get(pk=id_rating)
		except Rating.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# Se modifica al rating buscado
		rating.puntuacion = puntuacion
		rating.save()
		return Response({ 'mensaje': 'Rating modificado' }, status=status.HTTP_201_CREATED)

""" -------------------------------------------------------------------------------
	model Giro
--------------------------------------------------------------------------------"""
class GiroListAPIView(generics.ListCreateAPIView):
	queryset = Giro.objects.all()
	serializer_class = GiroSerializer

class GiroDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Giro.objects.all()
	serializer_class = GiroSerializer

@api_view(['POST'])
def VisitaAddAPIView(request):
	if request.method == 'POST':
		# Capturo los datos mandados por JSON
		id_afiliado = request.data['id_afiliado']

		# Intento buscar al usuario final y al afiliado objects
		try:
			afiliado = Afiliado.objects.get(pk=id_afiliado)
		except (UsuarioFinal.DoesNotExist, Afiliado.DoesNotExist):
			return Response(status=status.HTTP_404_NOT_FOUND)

		# Se crea un nuevo rating y se retorna un mensaje de creado
		afiliado.visitas = afiliado.visitas + 1
		afiliado.save()
		return Response({ 'mensaje': 'Visita aumentada' }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def ConteoGeneralAPIView(request):
	# Consultamos el total de afiliados, cupones y promociones activos
	afiliados_queryset = Afiliado.objects.filter(user__is_active=True).count()
	cupones_queryset = Cupon.objects.filter(status='Activo').count()
	promociones_queryset = Promocion.objects.filter(status='Activo').count()

	# Guardamos los querysets en un diccionario
	conteo_general = { 'numero_afiliados': afiliados_queryset, 'numero_cupones': cupones_queryset, 'numero_promociones': promociones_queryset }

	# Le pasamos el diccionario a nuestra clase Serializer
	serializer = ConteoGeneralSerializer(conteo_general)
	
	# Mostramos los datos
	return Response(serializer.data)


"""class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer"""
