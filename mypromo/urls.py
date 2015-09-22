from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView
from userprofiles.views import *
from cupones.views import AfiliadoCuponListView, CuponUpdateView
from promociones.views import AfiliadoPromocionListView, PromocionUpdateView

#from rest_framework import routers
from cupones.views import CuponAPIView, CuponAfiliadoAPIView, UsuariosCuponesDisponibles, CuponDetailAPIView, CuponPopularAPIView
from promociones.views import PromocionAPIView, PromocionAfiliadoAPIView, PromocionPopularAPIView
from rest_framework.urlpatterns import format_suffix_patterns

#router = routers.DefaultRouter()
#router.register(r'afiliados', AfiliadoViewSet.as_view())
#router.register(r'users', UserViewSet)
#router.register(r'grupos', GroupViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mypromo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/iniciar-sesion/$', 'userprofiles.views.iniciar_sesion'),
    url(r'^api/signup/$', SignupAPIView),
    url(r'^api/cambiar-clave/$', 'userprofiles.views.cambiar_clave'),
    url(r'^api/afiliados/$', AfiliadoAPIView.as_view()),
    url(r'^api/afiliados/(?P<pk>[0-9]+)/$', AfiliadoDetailAPIView.as_view()),
    #url(r'^api/afiliados-cupones-promociones/(?P<usuario>[0-9]+)/$', AfiliadoCuponesPromocionesAPIView),
    url(r'^api/afiliados-cupones/$', AfiliadoCuponesAPIView.as_view()),
    url(r'^api/afiliados-promociones/$', AfiliadoPromocionesAPIView.as_view()),
    url(r'^api/afiliados-carteles/$', AfiliadoCartelAPIView.as_view()),
    url(r'^api/locales/(?P<local_afiliado>[0-9]+)/$', LocalAfiliadoAPIView.as_view()),
    url(r'^api/cupones/$', CuponAPIView.as_view()),
    url(r'^api/cupon-popular/$', CuponPopularAPIView),
    url(r'^api/cupones/(?P<cupon_afiliado>[0-9]+)/$', CuponAfiliadoAPIView.as_view()),
    url(r'^api/cupones-detail/(?P<pk>[0-9]+)/$', CuponDetailAPIView.as_view(), name='cupon_detail_api'),
    url(r'^api/cupones-disponibles/(?P<usuario>[0-9]+)/$', UsuariosCuponesDisponibles.as_view()),
    url(r'^api/afiliados-disponibles/(?P<usuario>[0-9]+)/$', UsuariosCuponesAfiliados.as_view()),
    url(r'^api/usuarios-cupones/$', 'cupones.views.UsuariosCuponesAgregar'),
    url(r'^api/usuarios-promociones/$', 'promociones.views.UsuariosPromocionesAgregar'),
    url(r'^api/promociones/$', PromocionAPIView.as_view()),
    url(r'^api/promocion-popular/$', PromocionPopularAPIView),
    url(r'^api/promociones/(?P<promocion_afiliado>[0-9]+)/$', PromocionAfiliadoAPIView.as_view()),
    url(r'^api/correos/(?P<username>[\w\-]+)/$', CorreoUsuarioFinalAPIView.as_view()),
    url(r'^api/rating/(?P<usuario>[0-9]+)/$', RatingUsuarioFinalAPIView),
    url(r'^api/rating-create/$', RatingCreateAPIView),
    url(r'^api/rating-update/$', RatingUpdateAPIView),
    url(r'^api/giros/$', GiroListAPIView.as_view()),
    url(r'^api/giros/(?P<pk>[0-9]+)/$', GiroDetailAPIView.as_view()),
    url(r'^api/visitas-add/$', VisitaAddAPIView),
    url(r'^api/conteo-general/$', ConteoGeneralAPIView),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^password-reset/', include('password_reset.urls')),
    url(r'^admin/', include(admin.site.urls)), # URL para la vista del admin de Django
    
    
    #url(r'^signup/','userprofiles.views.signup', name='signup'),
    #url(r'^home/$', TemplateView.as_view(template_name='base.html'), name='home'),


    url(r'^$', RedirectView.as_view(url='/home/'), name='redirect_home'), # URL raiz que te redirecciona al Home si estas logueado
    url(r'^signup/$', SignupView, name='signup'), # URL para entrar al Login de MyPromo
    url(r'^login/$', LoginUserPromotorView.as_view(), name='login'), # URL para entrar al Login de MyPromo
    url(r'^logout/$', 'userprofiles.views.logout_view', name='logout'), # URL para desloguearse de MyPromo
    url(r'^enviar-correo/$', 'userprofiles.views.enviar_correo', name='enviar_correo'), # URL del home de MyPromo para afiliados

    # App userprofiles ----------------------------------------------------------------------------------------------------
    url(r'^home/$', 'userprofiles.views.home', name='home'), # URL del home de MyPromo
    url(r'^agregar-usuarios/$', 'userprofiles.views.RegisterUsuarioFinalView', name='agregar'), # URL para agregar usuarios finales
    url(r'^modificar/(?P<pk>[0-9]+)/$', UsuarioFinalUpdateView, name='usuario_modificar'), # URL para modificar el cupon seleccionado
    url(r'^agregar-afiliados/$', 'userprofiles.views.AfiliadoView', name='agregar_afiliados'), # URL para agregar afiliados
    url(r'^modificar-afiliado/(?P<usuario>[\w\-]+)/(?P<id>[0-9]+)/$', 'userprofiles.views.AfiliadoUpdateView', name='agregar_afiliados'), # URL para agregar afiliados
    url(r'^agregar-locales/(?P<usuario>[\w\-]+)/(?P<id_usuario>\d+)/$', 'userprofiles.views.LocalView', name='agregar_locales'), # URL para agregar locales
    url(r'^modificar-locales/(?P<usuario>[\w\-]+)/(?P<id>[0-9]+)/$', 'userprofiles.views.LocalUpdateView', name='modificar_locales'), # URL para modificar locales del afiliado
    url(r'^lista-locales/(?P<usuario>[\w\-]+)/(?P<id>[0-9]+)/$', 'userprofiles.views.LocalListDeleteView', name='lista_locales'), # URL para modificar locales del afiliado
    url(r'^lista-usuarios/$', UsuarioFinalListView.as_view(), name='lista_usuarios'), # URL para ver lista de usuarios finales
    url(r'^lista-afiliados/$', AfiliadoListView.as_view(), name='lista_afiliados'), # URL para ver lista de usuarios afiliados
    url(r'^administrar-usuarios/$', 'userprofiles.views.PromotorView', name='promotor_administrar'), # URL para agregar usuarios finales
    url(r'^agregar-promotores/$', 'userprofiles.views.PromotorCreateView', name='promotor_agregar'), # URL para agregar usuarios promotores
    url(r'^modificar-promotor/(?P<pk>[0-9]+)/$', 'userprofiles.views.PromotorUpdateView', name='promotor_modificar'), # URL para modificar el cupon seleccionado
    url(r'^modificar-status/(?P<pk>[\w\-]+)/$', StatusUpdateView.as_view(), name='status_modificar'), # URL para modificar el cupon seleccionado
    url(r'^scancards/$', ScanCardListView.as_view(), name='scancards_afiliados'),
    url(r'^scancards/(?P<pk>[0-9]+)/$', ScanCardView.as_view(), name='afiliado_scancard'),

    # App cupones -------------------------------------------------------------------------------------------------------------
    url(r'^cupones/', include('cupones.urls')), # URL para ver lista de usuarios afiliados y ver sus cupones

    # App promociones -------------------------------------------------------------------------------------------------------------
    url(r'^promociones/', include('promociones.urls')), # URL para ver lista de usuarios afiliados y ver sus promociones

    url(r'^(?P<usuario>[\w\-]+)/$', 'userprofiles.views.home_afiliado', name='home_afiliado'), # URL del home de MyPromo para afiliados
    url(r'^(?P<afiliado>[\w\-]+)/cupones/$', 'cupones.views.CuponView', { 'tipo_usuario': 'afiliado', 'plantilla': 'afiliado_cupones.html' }), # URL del home de MyPromo para afiliados
    url(r'^(?P<afiliado>[\w\-]+)/cupones/agregar/$', 'cupones.views.agregar_cupon', { 'tipo_usuario': 'afiliado', 'plantilla': 'afiliado_agregar_cupon.html' }), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/cupones/(?P<pk>[\w\-]+)/modificar/$', 'cupones.views.CuponView', name='afiliado_cupones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/promociones/$', 'promociones.views.AfiliadoPromocionView', name='afiliado_promociones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/promociones/agregar/$', 'promociones.views.agregar_promocion_afiliado', name='afiliado_cupones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/scancard/$', TemplateView.as_view(template_name='scancard.html'), name='scancard_afiliado'), # URL para modificar el cupon seleccionado
    url(r'^(?P<usuario>[\w\-]+)/administrar/$', 'userprofiles.views.AdministrarPerfilAfiliadoView', name='afiliado_administrar'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/locales/$', 'userprofiles.views.AfiliadoLocalDeleteView', name='afiliado_locales'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/locales/agregar/$', 'userprofiles.views.AfiliadoLocalUpdateView', name='afiliado_locales_agregar'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/estadisticas/$', 'userprofiles.views.AfiliadoEstadisticasView', name='afiliado_estadisticas'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/password/$', 'userprofiles.views.AfiliadoPasswordChangeView', name='afiliado_password'), # URL del home de MyPromo para afiliados


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
