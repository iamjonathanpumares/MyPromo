from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from userprofiles.views import UsuarioPromotorListView, UsuarioFinalListView, AfiliadoListView, LoginUserPromotorView, LocalView, StatusUpdateView
from cupones.views import AfiliadoCuponListView, CuponUpdateView
from promociones.views import AfiliadoPromocionListView, PromocionUpdateView

#from rest_framework import routers
from userprofiles.views import AfiliadoAPIView, AfiliadoDetailAPIView, AfiliadoCuponesAPIView, AfiliadoPromocionesAPIView, AfiliadoCartelAPIView, LocalAfiliadoAPIView, CorreoUsuarioFinalAPIView, UsuariosCuponesAfiliados
from cupones.views import CuponAPIView, CuponAfiliadoAPIView, UsuariosCuponesDisponibles
from promociones.views import PromocionAPIView, PromocionAfiliadoAPIView
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
    url(r'^api/cambiar-clave/$', 'userprofiles.views.cambiar_clave'),
    url(r'^api/afiliados/$', AfiliadoAPIView.as_view()),
    url(r'^api/afiliados/(?P<pk>[0-9]+)/$', AfiliadoDetailAPIView.as_view()),
    url(r'^api/afiliados-cupones/$', AfiliadoCuponesAPIView.as_view()),
    url(r'^api/afiliados-promociones/$', AfiliadoPromocionesAPIView.as_view()),
    url(r'^api/afiliados-carteles/$', AfiliadoCartelAPIView.as_view()),
    url(r'^api/locales/(?P<local_afiliado>[0-9]+)/$', LocalAfiliadoAPIView.as_view()),
    url(r'^api/cupones/$', CuponAPIView.as_view()),
    url(r'^api/cupones/(?P<cupon_afiliado>[0-9]+)/$', CuponAfiliadoAPIView.as_view()),
    url(r'^api/cupones-disponibles/(?P<usuario>[0-9]+)/$', UsuariosCuponesDisponibles.as_view()),
    url(r'^api/afiliados-disponibles/(?P<usuario>[0-9]+)/$', UsuariosCuponesAfiliados.as_view()),
    url(r'^api/usuarios-cupones/$', 'cupones.views.UsuariosCuponesAgregar'),
    url(r'^api/usuarios-promociones/$', 'promociones.views.UsuariosPromocionesAgregar'),
    url(r'^api/promociones/$', PromocionAPIView.as_view()),
    url(r'^api/promociones/(?P<promocion_afiliado>[0-9]+)/$', PromocionAfiliadoAPIView.as_view()),
    url(r'^api/correos/(?P<username>[\w\-]+)/$', CorreoUsuarioFinalAPIView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^password-reset/', include('password_reset.urls')),
    url(r'^admin/', include(admin.site.urls)), # URL para la vista del admin de Django
    
    
    #url(r'^signup/','userprofiles.views.signup', name='signup'),
    #url(r'^home/$', TemplateView.as_view(template_name='base.html'), name='home'),


    url(r'^$', RedirectView.as_view(url='/home/'), name='redirect_home'), # URL raiz que te redirecciona al Home si estas logueado
    url(r'^login/$', LoginUserPromotorView.as_view(), name='login'), # URL para entrar al Login de MyPromo
    url(r'^logout/$', 'userprofiles.views.logout_view', name='logout'), # URL para desloguearse de MyPromo
    url(r'^enviar-correo/$', 'userprofiles.views.enviar_correo', name='enviar_correo'), # URL del home de MyPromo para afiliados

    # App userprofiles ----------------------------------------------------------------------------------------------------
    url(r'^home/$', 'userprofiles.views.home', name='home'), # URL del home de MyPromo
    url(r'^agregar-usuarios/$', 'userprofiles.views.RegisterUsuarioFinalView', name='agregar'), # URL para agregar usuarios finales
    url(r'^agregar-afiliados/$', 'userprofiles.views.AfiliadoView', name='agregar_afiliados'), # URL para agregar afiliados
    url(r'^modificar-afiliado/(?P<usuario>[\w\-]+)/(?P<id>[0-9]+)/$', 'userprofiles.views.AfiliadoUpdateView', name='agregar_afiliados'), # URL para agregar afiliados
    url(r'^agregar-locales/(?P<usuario>[\w\-]+)/(?P<id_usuario>\d+)/$', 'userprofiles.views.LocalView', name='agregar_locales'), # URL para agregar locales
    url(r'^modificar-locales/(?P<usuario>[\w\-]+)/(?P<id>[0-9]+)/$', 'userprofiles.views.LocalUpdateView', name='agregar_locales'), # URL para modificar locales del afiliado
    url(r'^lista-usuarios/$', UsuarioFinalListView.as_view(), name='lista_usuarios'), # URL para ver lista de usuarios finales
    url(r'^lista-afiliados/$', AfiliadoListView.as_view(), name='lista_afiliados'), # URL para ver lista de usuarios afiliados
    url(r'^administrar-usuarios/$', 'userprofiles.views.PromotorView', name='promotor_administrar'), # URL para agregar usuarios finales
    url(r'^modificar-status/(?P<pk>[\w\-]+)/$', StatusUpdateView.as_view(), name='status_modificar'), # URL para modificar el cupon seleccionado

    # App cupones -------------------------------------------------------------------------------------------------------------
    url(r'^cupones/', include('cupones.urls')), # URL para ver lista de usuarios afiliados y ver sus cupones

    # App promociones -------------------------------------------------------------------------------------------------------------
    url(r'^promociones/', include('promociones.urls')), # URL para ver lista de usuarios afiliados y ver sus promociones

    url(r'^(?P<usuario>[\w\-]+)/$', 'userprofiles.views.home_afiliado', name='home_afiliado'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/cupones/$', 'cupones.views.AfiliadoCuponView', name='afiliado_cupones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/cupones/agregar/$', 'cupones.views.agregar_cupon_afiliado', name='afiliado_cupones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/cupones/(?P<pk>[\w\-]+)/modificar/$', 'cupones.views.AfiliadoCuponView', name='afiliado_cupones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/promociones/$', 'promociones.views.AfiliadoPromocionView', name='afiliado_promociones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/promociones/agregar/$', 'promociones.views.agregar_promocion_afiliado', name='afiliado_cupones'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/administrar/$', 'userprofiles.views.AdministrarPerfilAfiliadoView', name='afiliado_administrar'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/locales/$', 'userprofiles.views.AfiliadoLocalDeleteView', name='afiliado_locales'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/locales/agregar/$', 'userprofiles.views.AfiliadoLocalUpdateView', name='afiliado_locales'), # URL del home de MyPromo para afiliados
    url(r'^(?P<usuario>[\w\-]+)/password/$', 'userprofiles.views.AfiliadoPasswordChangeView', name='afiliado_password'), # URL del home de MyPromo para afiliados


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
