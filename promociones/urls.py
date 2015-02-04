from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
	# App promociones -------------------------------------------------------------------------------------------------------------
    url(r'^$', views.AfiliadoPromocionListView.as_view(), name='promociones'), # URL para ver lista de usuarios afiliados y ver sus promociones
    url(r'^lista/(?P<afiliado>[\w\-]+)/$', 'promociones.views.PromocionView', name='promociones_afiliado'), # URL para ver lista de promociones de cada afiliado
    url(r'^agregar/(?P<afiliado>[\w\-]+)/$', 'promociones.views.agregar_promocion', name='promociones_agregar'), # URL para ver lista de promociones de cada afiliado
    url(r'^(?P<pk>[\w\-]+)/modificar/$', views.PromocionUpdateView.as_view(), name='promocion_modificar'), # URL para modificar la promocion seleccionada
)