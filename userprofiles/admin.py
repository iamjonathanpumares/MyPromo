from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User

from .models import *

"""class AfiliadoInline(admin.StackedInline):
	model = Afiliado
	can_delete = False
	verbose_name_plural = 'afiliado'

class UserAdmin(UserAdmin):
	inlines = (AfiliadoInline, )

admin.site.unregister(User)"""
admin.site.register(Afiliado)
admin.site.register(Giro)
# admin.site.register(Promotor)
# admin.site.register(UsuarioFinal)
# admin.site.register(Rating)
