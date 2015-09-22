from django.contrib import admin

from .models import *

class LocalAdmin(admin.ModelAdmin):
	list_filter = ('afiliado',)

admin.site.register(Local, LocalAdmin)