from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):
	@method_decorator(login_required(login_url='/login/'))
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class PermissionRequiredMixin(object):
	permission = None

	@method_decorator(permission_required(permission, login_url='/login/'))
	def dispatch(self, request, *args, **kwargs):
		return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)