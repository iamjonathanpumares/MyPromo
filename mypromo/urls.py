from django.conf.urls import patterns, include, url
from django.contrib import admin
from userprofiles.views import UsuarioPromotorListView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mypromo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^signup/','userprofiles.views.signup', name='signup'),
    #url(r'^home/$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^agregar/$', 'userprofiles.views.RegisterUsuarioPromotorView', name='agregar'),
    url(r'^lista-usuarios/$', UsuarioPromotorListView.as_view(), name='agregar'),
)
