from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from userprofiles.forms import RegistrationUsuarioPromotorForm
from django.contrib.messages.views import SuccessMessageMixin
from .models import UsuarioPromotor

class RegistrationUserPromotorView(SuccessMessageMixin, FormView):
	model = UsuarioPromotor
	form_class = RegistrationUsuarioPromotorForm
	template_name = 'usuarios_agregar.html'
	success_url = '/agregar/'
	success_message = 'El usuario %s se ha creado correctamente en el modelo'

	def form_valid(self, form):
		form.save()
		return super(RegistrationUserPromotorView, self).form_valid(form)

	def get_success_message(self, cleaned_data):
		return self.success_message % cleaned_data['username']

	#return render(request, 'nuevousuario.html', {'form': form})