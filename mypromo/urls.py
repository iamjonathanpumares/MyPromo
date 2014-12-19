from django.conf.urls import patterns, include, url
from django.contrib import admin
from userprofiles.views import UsuarioPromotorListView, LoginUserPromotorView, LocalView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mypromo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)), # URL para la vista del admin de Django
    #url(r'^signup/','userprofiles.views.signup', name='signup'),
    #url(r'^home/$', TemplateView.as_view(template_name='base.html'), name='home'),


    url(r'^entrar/$', LoginUserPromotorView.as_view(), name='entrar'), # URL para entrar al Login de MyPromo

    # App userprofiles ----------------------------------------------------------------------------------------------------
    url(r'^agregar-usuarios/$', 'userprofiles.views.RegisterUsuarioPromotorView', name='agregar'), # URL para agregar usuarios finales
    url(r'^agregar-afiliados/$', 'userprofiles.views.AfiliadoView', name='agregar_afiliados'), # URL para agregar afiliados
    url(r'^agregar-locales/$', LocalView.as_view(), name='agregar_locales'), # URL para agregar locales
    url(r'^lista-usuarios/$', UsuarioPromotorListView.as_view(), name='agregar'), # URL para ver lista de usuarios finales
)
