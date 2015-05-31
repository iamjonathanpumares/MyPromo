from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
	# App cupones -------------------------------------------------------------------------------------------------------------
    url(r'^$', views.AfiliadoCuponListView.as_view(), name='cupones'), # URL para ver lista de usuarios afiliados y ver sus cupones
    url(r'^lista/(?P<afiliado>[\w\-]+)/$', 'cupones.views.CuponView', { 'tipo_usuario': 'promotor', 'plantilla': 'cupones.html' }), # URL para ver lista de cupones de cada afiliado
    url(r'^agregar/(?P<afiliado>[\w\-]+)/$', 'cupones.views.agregar_cupon', { 'tipo_usuario': 'promotor', 'plantilla': 'agregar_cupon.html' }), # URL para ver lista de cupones de cada afiliado
    url(r'^(?P<pk>[\w\-]+)/modificar/$', views.CuponUpdateView.as_view(), name='cupon_modificar'), # URL para modificar el cupon seleccionado
)