from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from userprofiles.views import UsuarioPromotorListView, UsuarioFinalListView, AfiliadoListView, LoginUserPromotorView, LocalView
from cupones.views import AfiliadoCuponListView, CuponUpdateView
from promociones.views import AfiliadoPromocionListView, PromocionUpdateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mypromo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)), # URL para la vista del admin de Django
    #url(r'^signup/','userprofiles.views.signup', name='signup'),
    #url(r'^home/$', TemplateView.as_view(template_name='base.html'), name='home'),


    url(r'^$', RedirectView.as_view(url='/home/'), name='redirect_home'), # URL raiz que te redirecciona al Home si estas logueado
    url(r'^login/$', LoginUserPromotorView.as_view(), name='login'), # URL para entrar al Login de MyPromo
    url(r'^logout/$', 'userprofiles.views.logout_view', name='logout'), # URL para desloguearse de MyPromo

    # App userprofiles ----------------------------------------------------------------------------------------------------
    url(r'^home/$', 'userprofiles.views.home', name='home'), # URL del home de MyPromo
    url(r'^agregar-usuarios/$', 'userprofiles.views.RegisterUsuarioFinalView', name='agregar'), # URL para agregar usuarios finales
    url(r'^agregar-afiliados/$', 'userprofiles.views.AfiliadoView', name='agregar_afiliados'), # URL para agregar afiliados
    url(r'^agregar-locales/(?P<usuario>[\w\-]+)/(?P<id_usuario>\d+)/$', 'userprofiles.views.LocalView', name='agregar_locales'), # URL para agregar locales
    url(r'^lista-usuarios/$', UsuarioFinalListView.as_view(), name='lista_usuarios'), # URL para ver lista de usuarios finales
    url(r'^lista-afiliados/$', AfiliadoListView.as_view(), name='lista_afiliados'), # URL para ver lista de usuarios afiliados
    url(r'^administrar-usuarios/$', 'userprofiles.views.PromotorView', name='promotor_administrar'), # URL para agregar usuarios finales

    # App cupones -------------------------------------------------------------------------------------------------------------
    url(r'^cupones/$', AfiliadoCuponListView.as_view(), name='cupones'), # URL para ver lista de usuarios afiliados y ver sus cupones
    url(r'^cupones/(?P<afiliado>[\w\-]+)/$', 'cupones.views.CuponView', name='cupones_afiliado'), # URL para ver lista de cupones de cada afiliado
    url(r'^cupones/(?P<pk>[\w\-]+)/modificar/$', CuponUpdateView.as_view(), name='cupon_modificar'), # URL para modificar el cupon seleccionado

    # App promociones -------------------------------------------------------------------------------------------------------------
    url(r'^promociones/$', AfiliadoPromocionListView.as_view(), name='promociones'), # URL para ver lista de usuarios afiliados y ver sus promociones
    url(r'^promociones/(?P<afiliado>[\w\-]+)/$', 'promociones.views.PromocionView', name='promociones_afiliado'), # URL para ver lista de promociones de cada afiliado
    url(r'^promociones/(?P<pk>[\w\-]+)/modificar/$', PromocionUpdateView.as_view(), name='promocion_modificar'), # URL para modificar la promocion seleccionada

    url(r'^(?P<usuario>[\w\-]+)/$', 'userprofiles.views.home_afiliado', name='home_afiliado'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/cupones/$', 'cupones.views.AfiliadoCuponView', name='afiliado_cupones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/cupones/(?P<pk>[\w\-]+)/modificar/$', 'cupones.views.AfiliadoCuponView', name='afiliado_cupones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/promociones/$', 'promociones.views.AfiliadoPromocionView', name='afiliado_promociones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/administrar/$', 'userprofiles.views.AdministrarAfiliadoView', name='afiliado_administrar'), # URL del home de MyPromo para afiliados
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
