from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.views.generic import ListView, FormView
from userprofiles.forms import RegistrationUsuarioPromotorForm
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import LoginForm

class LoginUserPromotorView(FormView):
	#model = UsuarioPromotor
	template_name = 'login.html'
	success_url = '/agregar/'
	form_class = LoginForm

	def form_valid(self, form):
		#login(self.request, form.get_user())
		return super(LoginUserPromotorView, self).form_valid(form)

class UsuarioPromotorListView(ListView):
	model = User
	template_name = 'lista_usuarios.html'

def RegisterUsuarioPromotorView(request): # Vista encargada de mostrar el formulario de registro
	if request.method == 'POST': # Verifica si la peticion hecha por el usuario es POST
		form = RegistrationUsuarioPromotorForm(data=request.POST) # Creamos una instancia y le pasamos los datos del formulario
		if form.is_valid(): # Verificar si los campos fueron validados correctamente
			user = form.save() # Guarda un usuario con los datos dados en el formulario
			usuario = form.cleaned_data['username'] # Guardamos el nombre del usuario con ayuda de la variable cleaned_data
			messages.info(request, 'Usuario %s agregado correctamente' % usuario) # Creamos un mensaje de exito para mostrarlo en la otra vista
			return redirect('/lista-usuarios/') # Nos redirijimos a la vista lista_usuarios
	else:
			form = RegistrationUsuarioPromotorForm() # En caso de no ser una peticion POST se crea la instancia del formulario
	return render_to_response('usuarios_agregar.html', { 'form': form }, context_instance=RequestContext(request)) # Renderizamos el formulario para que se muestra en el template

def lista_usuarios_view(request):
	return render(request, 'lista_usuarios.html')