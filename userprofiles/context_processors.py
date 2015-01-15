from .models import Afiliado
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

def datos_afiliado(request):
	try:
		request.user.groups.get(name='Afiliado')
	except Group.DoesNotExist:
		return { }
	else:
		usuario = request.user.username
		afiliado = get_object_or_404(Afiliado, user__username=usuario)
		return { 'afiliado': afiliado }