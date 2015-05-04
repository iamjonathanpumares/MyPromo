# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Cupon, UsuariosCupones

class CuponAdmin(admin.ModelAdmin):
	# Especificamos la lista de campos que queremos visualizar en la lista de cambios
	list_display = ('titulo', 'fecha_inicio', 'vigencia', 'status')

	# Incluimos una barra de búsqueda especificando los campos por los que queremos buscar
	search_fields = ('titulo',)

	# Se agregan filtros pasando una tupla con los campos con los que queremos filtrar
	list_filter = ('status', 'vigencia',)
	date_hierarchy = 'vigencia'

class UsuariosCuponesAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'cupon_usuario', 'fecha',)

admin.site.register(Cupon, CuponAdmin)
admin.site.register(UsuariosCupones, UsuariosCuponesAdmin)
