from django.contrib.auth.models import Group
from django.http import Http404
from django.shortcuts import redirect

def redirect_home(home):
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