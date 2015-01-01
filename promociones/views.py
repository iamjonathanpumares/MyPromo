from django.shortcuts import render
from django.views.generic import ListView
from userprofiles.models import Afiliado

class AfiliadoPromocionListView(ListView):
	model = Afiliado
	template_name = 'promociones_afiliados.html'
