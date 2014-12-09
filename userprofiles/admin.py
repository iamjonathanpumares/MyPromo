from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Afiliado

class AfiliadoInline(admin.StackedInline):
	model = Afiliado
	can_delete = False
	verbose_name_plural = 'afiliado'

class UserAdmin(UserAdmin):
	inlines = (AfiliadoInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
