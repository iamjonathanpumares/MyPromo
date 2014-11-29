from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from userprofiles.forms import RegistrationUsuarioPromotorForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import UsuarioPromotor

class RegistrationUserPromotorView(SuccessMessageMixin, CreateView):
	model = UsuarioPromotor
	#fields = ['username', 'nombre', 'apellidos', 'password']
	form_class = RegistrationUsuarioPromotorForm
	template_name = 'usuarios_agregar.html'
	#success_url = '/agregar/'
	success_message = 'El usuario %s se ha creado correctamente en el modelo'

	def form_valid(self, form):
		form.save()
		return super(RegistrationUserPromotorView, self).form_valid(form)

	def get_success_message(self, cleaned_data):
		return self.success_message % cleaned_data['username']

class UsuarioPromotorListView(ListView):
	model = UsuarioPromotor
	template_name = 'lista_usuarios.html'

def RegisterUsuarioPromotorView(request): # Vista encargada de mostrar el formulario de registro
	if request.method == 'POST': # Verifica si la peticion hecha por el usuario es POST
		form = RegistrationUsuarioPromotorForm(data=request.POST) # Creamos una instancia y le pasamos los datos del formulario
		if form.is_valid(): # Verificar si los campos fueron validados correctamente
			user = form.save() # Guarda un usuario con los datos dados en el formulario
			usuario = form.cleaned_data['username'] # Guardamos el nombre del usuario con ayuda de la variable cleaned_data
			messages.info(request, 'Usuario %s agregado correctamente' % usuario) # Creamos un mensaje de exito para mostrarlo en la otra vista
			return redirect('/lista-usuarios/') # Nos redirijimos a la vista lista_usuarios
			#return render_to_response('lista_usuarios.html', { 'save_success': save_success, 'usuario': usuario })
	else:
			form = RegistrationUsuarioPromotorForm() # En caso de no ser una peticion POST se crea la instancia del formulario
			form.fields['username'].widget.attrs = { 'class': 'form-control' } # Esto agrega un atributo class a cada widget para ponerle estilos
			form.fields['nombre'].widget.attrs = { 'class': 'form-control' }
			form.fields['apellidos'].widget.attrs = { 'class': 'form-control' }
			form.fields['password1'].widget.attrs = { 'class': 'form-control' }
			form.fields['password2'].widget.attrs = { 'class': 'form-control' }
	return render_to_response('usuarios_agregar.html', { 'form': form }, context_instance=RequestContext(request)) # Renderizamos el formulario para que se muestra en el template

def lista_usuarios_view(request):
	return render(request, 'lista_usuarios.html')