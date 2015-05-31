from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import Http404
from django.shortcuts import redirect

def redirect_home(home):
	@login_required(login_url='/login/')
	def wrapper(request):
		if request.user.is_superuser == True:
			return home(request)
		else:
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
				return home(request)

	return wrapper

def is_afiliado_or_404(funcion):
	@login_required(login_url='/login/')
	def wrapper(request, *args, **kwargs):
		tipo_usuario = kwargs.get('tipo_usuario', None)
		afiliado = kwargs.get('afiliado', None)
		if tipo_usuario == 'afiliado':
			if request.user.username == afiliado:
				return funcion(request, *args, **kwargs)
			else:
				raise Http404
		return funcion(request, *args, **kwargs)


	return wrapper